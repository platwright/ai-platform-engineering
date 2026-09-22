# Chapter 01 - Observability Layers for AI Systems

## The Standard Stack: MELT

Observability practitioners typically organize signals into four categories:

- **Metrics**: numeric measurements over time (request rate, error rate, latency p95)
- **Events**: discrete occurrences with structured data (model invocation, deployment, tool call)
- **Logs**: time-stamped records of what happened (structured request logs, error traces)
- **Traces**: correlated spans that show the path of a single request through distributed systems

These four pillars cover conventional software systems well. AI systems need extensions to each, plus a fifth pillar.

## Layer 1: Metrics

Standard infrastructure metrics apply fully:

- CPU and memory utilization
- HTTP request rate, error rate, latency
- Network throughput
- Container and pod health

AI-specific additions:

| Metric | Why It Matters |
|---|---|
| `prompt_tokens` | Input cost, context budget tracking |
| `completion_tokens` | Output cost, output length monitoring |
| `time_to_first_token` | User-perceived responsiveness |
| `generation_tokens_per_second` | Serving throughput capacity |
| `kv_cache_utilization` | GPU memory pressure indicator |
| `queue_depth` | Serving backlog before requests are processed |
| `cost_per_request` | Financial impact measurement |
| `retrieval_latency` | RAG pipeline contribution to total latency |
| `eval_score_trend` | Quality signal alongside reliability |

## Layer 2: Events

Events in AI systems that standard logging often misses:

- **Model invocation**: model name, version, provider, parameters used
- **Tool call**: tool name, arguments, success/failure, latency
- **Human approval**: approve or deny event, approver identity, tool action
- **Prompt version change**: old version, new version, deployer
- **Fallback triggered**: which model was the primary, which is the fallback, why
- **Cache hit**: prompt cache or semantic cache, savings realized
- **Eval run**: run ID, pass rate, comparison to baseline

Each event should carry the trace ID of the request it belongs to, enabling correlation with traces.

## Layer 3: Logs

Structured logs for AI workloads should include:

```json
{
  "timestamp": "2025-09-01T14:32:10Z",
  "trace_id": "abc123",
  "request_id": "req-456",
  "tenant": "team-a",
  "model": "gpt-4o-mini-2024-07-18",
  "prompt_version": "rag-grounding-v1.4.0",
  "prompt_tokens": 843,
  "completion_tokens": 142,
  "total_tokens": 985,
  "ttft_ms": 320,
  "total_latency_ms": 1840,
  "finish_reason": "stop",
  "cost_usd": 0.000714,
  "error": null
}
```

What to omit without scrubbing:

- full prompt text (may contain PII)
- full response text (may contain sensitive or biased content)
- user identifiers that go beyond pseudonymized session IDs

What to include conditionally (with access controls and scrubbing):

- truncated prompt preview (first 100 characters, PII-scrubbed)
- response category or classification label (not full text)

## Layer 4: Traces

Distributed traces show the full request path and latency composition. For AI systems, each layer of the stack should produce spans with AI-relevant attributes.

OpenTelemetry GenAI semantic conventions define standard span attributes for LLM calls:

```
gen_ai.system: "openai"
gen_ai.request.model: "gpt-4o-mini-2024-07-18"
gen_ai.request.max_tokens: 800
gen_ai.response.finish_reasons: ["stop"]
gen_ai.usage.prompt_tokens: 843
gen_ai.usage.completion_tokens: 142
```

A full RAG request trace might contain spans for:

1. `app.handle_chat` (root span)
2. `gateway.route_request`
3. `rag.embed_query`
4. `rag.vector_search`
5. `rag.rerank`
6. `llm.generate`

Each span records its own start time, end time, and any relevant attributes, giving a complete latency waterfall.

## Layer 5: Evaluations

Evaluation-driven observability is unique to AI systems. It asks: not just "did the system respond?" but "did the system respond correctly?"

Evaluation scores run as:

- **Offline scheduled jobs**: run the full eval suite daily and track the trend
- **Online sampled evaluation**: score a random sample of live requests
- **Triggered evaluation**: run evaluation automatically when a new prompt version deploys

Evaluation scores appear alongside runtime metrics on the platform dashboard and can trigger alerts when they fall below thresholds.

This is the layer that closes the gap between "the system is up" and "the system is working."

## The Gap Between Green And Correct

The most important reason to think beyond MELT is this: every layer of a well-instrumented AI platform can show green while the system produces poor-quality outputs.

- HTTP 200 status codes measure transport success, not content quality
- Low latency measures speed, not correctness
- High cache hit rates measure efficiency, not answer accuracy

An AI platform that observes only the first four layers will discover quality regressions through user complaints rather than monitoring. The fifth layer — evaluations — is what makes AI platforms operationally mature rather than operationally blind.
