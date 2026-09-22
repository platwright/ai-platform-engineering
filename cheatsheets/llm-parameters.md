# LLM Generation Parameters Cheatsheet

## Parameter Quick Reference

| Parameter | Type | Common Range | Effect |
|---|---|---|---|
| `temperature` | float | 0.0 – 2.0 | Output randomness (0 = deterministic, >1 = creative) |
| `top_p` | float | 0.0 – 1.0 | Nucleus sampling probability mass cutoff |
| `top_k` | integer | 1 – 200 | Token vocabulary cutoff |
| `max_tokens` | integer | 1 – model_max | Maximum output tokens |
| `stop` | list[str] | any strings | Halt generation at these sequences |
| `seed` | integer | any | Reproducibility hint |
| `frequency_penalty` | float | -2.0 – 2.0 | Reduce repeated tokens proportionally |
| `presence_penalty` | float | -2.0 – 2.0 | Flat penalty for any already-used token |

## Recommended Defaults By Use Case

| Use Case | temperature | top_p | max_tokens |
|---|---|---|---|
| Factual lookup | 0.1 | 0.9 | 200 |
| Conversational chat | 0.7 | 0.9 | 600 |
| Code generation | 0.2 | 0.95 | 2000 |
| Creative writing | 1.0 | 0.95 | 2000 |
| Structured data extraction | 0.0 | 1.0 | 500 |
| Classification | 0.0 | 1.0 | 20 |
| Summarization | 0.5 | 0.9 | 800 |
| Batch evaluation (eval judge) | 0.0 | 1.0 | 100 |

## Temperature Intuition

```
temperature=0.0   → almost always the top token (near-deterministic)
temperature=0.5   → focuses on likely tokens, rarely surprising
temperature=0.7   → balanced: coherent and occasionally varied
temperature=1.0   → raw model distribution (default behavior)
temperature=1.5   → noticeably varied, sometimes unusual word choices
temperature=2.0   → highly unpredictable, often incoherent for long text
```

## Max Tokens Safety

Always set `max_tokens`. Unbounded generation:
- On hosted APIs: creates unexpected cost spikes
- On self-hosted: causes GPU memory pressure and latency spikes
- For structured output: allows runaway generation that never closes the JSON

## Stop Sequences For Common Patterns

```json
// Stop at a turn delimiter
"stop": ["\n\nUser:", "\n\nHuman:"]

// Stop after a JSON close
"stop": ["\n}"]

// Stop after a code block
"stop": ["```"]

// Stop at a section header
"stop": ["###"]
```

## Structured Output Parameters

```json
// JSON mode (syntax valid, no schema enforcement)
"response_format": {"type": "json_object"}

// Schema-constrained (OpenAI structured outputs)
"response_format": {
  "type": "json_schema",
  "json_schema": {
    "name": "my_schema",
    "schema": { ... }
  }
}
```

## Tool Choice Values

```json
"tool_choice": "auto"      // model decides
"tool_choice": "required"  // must call a tool
"tool_choice": "none"      // never call a tool

// Force specific tool
"tool_choice": {
  "type": "function",
  "function": {"name": "get_metrics"}
}
```

## vLLM-Specific Parameters

| Parameter | Description |
|---|---|
| `guided_json` | JSON schema for constrained decoding |
| `guided_regex` | Regex pattern for output constraint |
| `guided_choice` | List of exact allowed output strings |
| `guided_grammar` | EBNF grammar for output constraint |
| `best_of` | Generate N candidates, return best one |

## Platform Logging Checklist

Log these fields from every production inference call:

- `model`
- `temperature`, `top_p`, `max_tokens`
- `prompt_tokens`, `completion_tokens`, `total_tokens`
- `finish_reason` (`stop`, `length`, `tool_calls`, `content_filter`)
- request latency (ms)
- TTFT (ms, if streaming)
