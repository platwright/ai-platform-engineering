# Chapter 03 - Distributed Tracing with LLM Context

## Why Distributed Tracing Matters For AI Systems

A production AI request may cross five or more service boundaries: the application server, the AI gateway, an embedding service, a vector database, a reranker, and the model server. When a user reports that a response was slow or wrong, which layer was responsible?

Without distributed tracing, the answer to that question involves guesswork, log correlation by timestamp, and significant engineering time. With end-to-end traces, the answer is one query away.

## OpenTelemetry For LLM Workloads

OpenTelemetry (OTel) is the standard instrumentation framework for distributed systems. It provides:

- **Traces**: correlated spans across services via propagated context
- **Metrics**: a vendor-neutral metric format
- **Logs**: structured log export with trace correlation

The OpenTelemetry GenAI Semantic Conventions define standard span attributes for LLM calls. Using these ensures traces are readable by any OTel-compatible backend (Jaeger, Tempo, Honeycomb, etc.).

## Standard LLM Span Attributes

For a span representing a model call, the GenAI semantic conventions specify:

| Attribute | Example | Description |
|---|---|---|
| `gen_ai.system` | `"openai"` | Model provider |
| `gen_ai.request.model` | `"gpt-4o-mini"` | Model name |
| `gen_ai.request.max_tokens` | `800` | Max output tokens requested |
| `gen_ai.request.temperature` | `0.3` | Temperature parameter |
| `gen_ai.response.id` | `"chatcmpl-abc123"` | Provider-assigned response ID |
| `gen_ai.response.finish_reasons` | `["stop"]` | Finish reason(s) |
| `gen_ai.usage.prompt_tokens` | `843` | Input token count |
| `gen_ai.usage.completion_tokens` | `142` | Output token count |

## Instrumenting A Python Service

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup (once at startup)
provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("ai-gateway")

def handle_chat_request(request: dict) -> dict:
    with tracer.start_as_current_span("gateway.handle_chat") as span:
        span.set_attribute("tenant", request["tenant"])
        span.set_attribute("prompt_version", request.get("prompt_version", "unknown"))

        # Retrieval span
        with tracer.start_as_current_span("rag.retrieve") as rag_span:
            chunks = retrieve(request["question"])
            rag_span.set_attribute("rag.chunks_returned", len(chunks))
            rag_span.set_attribute("rag.service_name", request["service_name"])

        # LLM call span
        with tracer.start_as_current_span("llm.generate") as llm_span:
            llm_span.set_attribute("gen_ai.system", "openai")
            llm_span.set_attribute("gen_ai.request.model", request["model"])
            response = call_model(request)
            llm_span.set_attribute("gen_ai.usage.prompt_tokens", response.usage.prompt_tokens)
            llm_span.set_attribute("gen_ai.usage.completion_tokens", response.usage.completion_tokens)

        return {"response": response.content}
```

## Context Propagation

For traces to connect across services, the trace context must be propagated in HTTP headers:

```python
from opentelemetry.propagate import inject, extract
from opentelemetry import context

# When making an outgoing HTTP call, inject the current trace context
headers = {}
inject(headers)
response = requests.post(upstream_url, json=payload, headers=headers)

# When receiving an incoming HTTP call, extract and attach the trace context
incoming_ctx = extract(request.headers)
token = context.attach(incoming_ctx)
```

Standard propagation uses the W3C `traceparent` header format, which is supported by all major OTel-compatible frameworks.

## Sampling Strategies

Full tracing of every request at scale produces large volumes of data. Sampling reduces costs:

### Head-Based Sampling

Decide at the start of a request whether to sample it. Simple and low-overhead but loses potentially interesting traces before knowing they are interesting.

```yaml
# OTel Collector config
processors:
  probabilistic_sampler:
    sampling_percentage: 10  # sample 10% of all requests
```

### Tail-Based Sampling

Collect all spans but decide at the end of a trace whether to keep it. Allows keeping all slow or error traces regardless of the baseline sampling rate.

```yaml
processors:
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: keep-errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: keep-slow
        type: latency
        latency: { threshold_ms: 2000 }
      - name: sample-rest
        type: probabilistic
        probabilistic: { sampling_percentage: 5 }
```

Tail-based sampling is more complex to configure but provides much better signal-to-cost ratio for AI platforms where most requests are fast and healthy.

## Trace Storage and Analysis

| Tool | Type | Notes |
|---|---|---|
| Jaeger | Self-hosted | Good for local development and learning |
| Grafana Tempo | Self-hosted | Integrates well with Grafana dashboards |
| Honeycomb | SaaS | Excellent trace query and exploration interface |
| AWS X-Ray | Cloud | AWS-native, deep integration with managed services |
| Google Cloud Trace | Cloud | GCP-native |

For the course local stack, Jaeger provides an accessible interface for exploring traces without cloud dependencies.

## Correlating Traces With Logs And Metrics

The trace ID should appear in:

- all structured log entries for that request
- any metrics labeled with `request_id`
- any eval run results for that session

This correlation is what makes a query like "show me all system behavior for this specific request that received negative user feedback" possible.
