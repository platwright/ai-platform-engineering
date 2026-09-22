# Module 02 Solution

## Expected Token Count Relationships

For the lab exercise comparing system prompt lengths:

A system prompt of roughly 30 words will produce approximately 40–50 tokens.

A system prompt of roughly 90 words (the extended version) will produce approximately 120–140 tokens.

The difference is 80–100 tokens. At $5 per million tokens, that is $0.0004 per request. At 10,000 requests per day, the difference becomes approximately $1.50/day or $550/year for that one system prompt change.

This is why prompt engineering and token budgeting are not purely academic concerns.

## Expected Run Artifact Structure

A successful run artifact from Project 01 will include a structure similar to:

```json
{
  "provider": "acme-fast",
  "message": "Explain what a context window is in one sentence.",
  "response": "A context window is the maximum amount of text a language model can process at one time, measured in tokens.",
  "usage": {
    "prompt_tokens": 47,
    "completion_tokens": 22,
    "total_tokens": 69
  },
  "latency_ms": 312,
  "timestamp": "2025-09-01T14:32:10Z"
}
```

If your artifact does not include a `usage` field, the provider adapter is not capturing token metadata. That is a gap worth noting.

## Tool Schema Reference Answers

### query_rag

```json
{
  "name": "query_rag",
  "description": "Retrieve relevant document chunks from a named knowledge base. Use this when the user asks about domain-specific content that may be in the knowledge base.",
  "parameters": {
    "type": "object",
    "properties": {
      "service_name": {
        "type": "string",
        "description": "The registered RAG service name, e.g. 'team-a-kb'."
      },
      "question": {
        "type": "string",
        "description": "The natural language question to search for."
      },
      "top_k": {
        "type": "integer",
        "description": "Maximum number of chunks to return. Defaults to 5.",
        "default": 5
      }
    },
    "required": ["service_name", "question"]
  }
}
```

Approval required: no (read-only).

### scale_deployment

```json
{
  "name": "scale_deployment",
  "description": "Adjust the replica count for a named Kubernetes deployment. This modifies live infrastructure and requires explicit operator approval.",
  "parameters": {
    "type": "object",
    "properties": {
      "deployment_name": {
        "type": "string",
        "description": "The name of the Kubernetes deployment to scale."
      },
      "namespace": {
        "type": "string",
        "description": "The Kubernetes namespace containing the deployment."
      },
      "replicas": {
        "type": "integer",
        "description": "Target replica count. Must be 0 or greater.",
        "minimum": 0
      }
    },
    "required": ["deployment_name", "namespace", "replicas"]
  }
}
```

Approval required: yes — scaling to 0 is destructive; scaling up has cost implications.

## Model Routing Reference Answers

1. **Customer support chatbot at 2M tokens/day, no PII**: self-hosted large model. Volume justifies infrastructure investment; no privacy blocker.
2. **HR assistant with employee records**: self-hosted — data sovereignty requirements. Privacy makes hosted APIs risky regardless of cost.
3. **Code review tool needing strong reasoning**: hosted frontier model initially. Complex reasoning benefits from frontier capability; evaluate self-hosted options as open-weight models improve.
4. **Document classifier, 12 categories**: self-hosted small model. Classification is a well-bounded task where a fine-tuned small model often outperforms general large models.
5. **Batch summarization, 50K documents/week**: self-hosted for cost efficiency. Batch jobs tolerate latency, and the predictable volume makes infrastructure investment straightforward.

## Streaming Verification Reference

If you could not find streaming support in the gateway:

The gateway's chat endpoint likely buffers the entire response from the upstream provider before returning it to the client. That works for non-streaming clients but adds latency equal to the full generation time before the first byte arrives.

To add streaming support, the gateway response path needs to:
1. Set `stream: true` in the upstream request
2. Set `Content-Type: text/event-stream` on the response
3. Relay each SSE chunk immediately without buffering
4. Buffer the response independently (as a background operation) for logging and usage accounting
