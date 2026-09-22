# Chapter 03 - Structured Outputs

## Why Structure Matters For Platform Work

LLM responses are text by default. When a system needs to parse, route, or act on model output programmatically, free-form text is fragile.

Structured output capabilities let models produce valid JSON, follow a schema, or fill a template reliably enough to be processed without heroic parsing logic.

This matters for platform engineers because:

- structured outputs are the bridge between LLM responses and API responses
- downstream services depend on predictable shapes
- validation and error handling become explicit instead of buried in regex

## JSON Mode

JSON mode is the simplest structured output capability. When enabled, the model constrains its output to be syntactically valid JSON.

Request:
```json
{
  "model": "gpt-4o-mini",
  "response_format": {"type": "json_object"},
  "messages": [
    {"role": "system", "content": "Return a JSON object with fields: topic, summary, and sentiment."},
    {"role": "user",   "content": "Summarize this text about container resource limits."}
  ]
}
```

JSON mode guarantees:
- syntactically valid JSON
- no wrapping markdown fences or prose preamble

JSON mode does not guarantee:
- specific fields are present
- field names match your schema
- values are the right type

The model will still hallucinate field names or omit expected keys if the prompt is ambiguous.

## Schema-Constrained Generation (Structured Outputs)

A stronger capability is schema-constrained generation, where the model is constrained to produce output that matches a specific JSON Schema.

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "incident_summary",
    "schema": {
      "type": "object",
      "properties": {
        "severity":    {"type": "string", "enum": ["P1", "P2", "P3"]},
        "service":     {"type": "string"},
        "root_cause":  {"type": "string"},
        "resolved":    {"type": "boolean"}
      },
      "required": ["severity", "service", "root_cause", "resolved"],
      "additionalProperties": false
    }
  }
}
```

When schema-constrained generation is available (OpenAI structured outputs, Anthropic tool use, Gemini response schema), the model is guided by constrained decoding that actively enforces the schema at each token step.

This is significantly more reliable than JSON mode alone and is the correct approach for production parsing pipelines.

## Constrained Decoding (How It Works)

Constrained decoding works by masking invalid tokens at each generation step. The model can only produce tokens that could lead to a valid output according to the grammar or schema.

For a JSON object with a required string field `"severity"`, the model is constrained to:
1. Open with `{`
2. Produce the key `"severity"`
3. Produce a colon
4. Produce one of the allowed enum values
5. And so on...

This happens at every token step. The model effectively loses its freedom to produce invalid JSON because those token sequences are masked from the distribution.

Constrained decoding eliminates most JSON parse failures. It does not eliminate semantic failures (wrong severity chosen for reasons the schema cannot capture).

## Tool Calling as Structured Output

Tool calling uses the same underlying mechanism. When a model produces a tool call, it outputs a structured object specifying:

- the tool name
- the arguments as a JSON object

```json
{
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "get_service_metrics",
        "arguments": "{\"service_name\": \"inference-gateway\", \"window\": \"1h\"}"
      }
    }
  ]
}
```

Tool calling is covered in more depth in the next chapter.

## Where Structured Outputs Break

Even with constrained decoding, structured output flows can fail:

| Failure mode | Description |
|---|---|
| Schema too complex | Very large or deeply nested schemas slow decoding and may degrade content quality |
| Semantic hallucination | The model produces valid JSON but wrong values |
| Missing context | The model cannot populate a required field because the information was never provided |
| Schema mismatch | The application schema and the model schema diverge over time |
| Streaming challenges | Parsing partial JSON during streaming requires buffered parsing logic |

## Validation Patterns

Never trust structured output without explicit validation:

```python
import json
from jsonschema import validate, ValidationError

def parse_and_validate(raw: str, schema: dict) -> dict:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model produced invalid JSON: {e}") from e

    try:
        validate(instance=parsed, schema=schema)
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e.message}") from e

    return parsed
```

Platform patterns for structured output pipelines:

1. Always validate against the schema after parsing, even with constrained decoding
2. Log the raw model response before parsing for debugging
3. Define retry behavior for validation failures (re-prompt with the error message)
4. Monitor schema validation failure rates as a quality signal

## Self-Hosted Model Considerations

Not all self-hosted model servers support constrained decoding equally:

- **vLLM**: supports guided decoding via `guided_json`, `guided_regex`, and `guided_grammar` parameters
- **Ollama**: supports JSON format mode; schema constraints vary by version
- **llama.cpp**: supports grammar-constrained generation with GBNF grammars
- **TGI (Text Generation Inference)**: supports JSON schema-constrained generation

Check the serving backend documentation for your deployed model before relying on strict schema enforcement in production.

## Summary

| Capability | Reliability | What It Guarantees |
|---|---|---|
| JSON mode | Moderate | Syntactically valid JSON |
| Schema constraints | High | Valid JSON matching the schema structure |
| Constrained decoding | High | Valid tokens at each step according to the grammar |
| Post-parse validation | Essential | Catches semantic failures schema cannot prevent |
