# Chapter 01 - End-to-End Latency Decomposition

## Why Decomposition Matters

A single "latency = 2,400ms" measurement tells you nothing about where time is spent. Latency decomposition breaks that 2,400ms into segments so you know which one to address.

The most common mistake in AI performance work is adding GPU replicas when the bottleneck is prompt length driving prefill time, or optimizing the model server when the real bottleneck is a slow embedding call in the RAG pipeline.

## The Full Request Waterfall

For a RAG-augmented chat request:

```
Stage                           Time        Notes
──────────────────────────────────────────────────────────────
1. Client → gateway (network)   5–20ms      Distance to gateway
2. Gateway auth + routing       5–15ms      JWT verify, route select
3. RAG: embed query             40–80ms     Embedding model call
4. RAG: vector search           10–30ms     Vector DB query
5. RAG: rerank                  50–200ms    Reranker model call
6. Gateway → model (network)    1–5ms       Internal network
7. Model queue wait             0 – ∞       Grows under load
8. Model prefill                50–500ms    Scales with prompt length
9. Time to first token (TTFT)   ←— measured here
10. Token generation            500–5000ms  output_tokens / tokens_per_second
11. Response transmission       5–20ms      Back to client
──────────────────────────────────────────────────────────────
Total                           ~700–6000ms
```

## Key Relationships

### Prefill Time Scales With Prompt Length

Prefill is the step where the model processes all input tokens and produces the KV cache. It scales roughly linearly with total input tokens:

```
prefill_time ≈ input_tokens × prefill_rate_per_token
# For a 7B model on an A10G:
# ~1ms per token for inputs up to ~8K, then grows super-linearly
```

A system prompt of 2,000 tokens + 1,000 tokens of retrieved context + 100 token user query = 3,100 token prefill.
A system prompt of 500 tokens + 50 token user query = 550 token prefill.

The first takes roughly 5× longer to prefill.

### Generation Time Scales With Output Length

After TTFT, each output token is generated sequentially:

```
generation_time = output_tokens / tokens_per_second

# 200 output tokens at 40 tok/s = 5 seconds
# 50 output tokens at 40 tok/s = 1.25 seconds
```

Setting a reasonable `max_tokens` limit reduces the worst-case generation time.

### Queue Wait Is Unbounded Without Backpressure

Under load, the model queue wait is the most variable component. When a GPU is serving 10 requests, the 11th waits. The 50th waits for 40 requests to finish. This is why queue depth is the key autoscaling signal.

## Measuring Each Component

Use distributed traces (Module 12) to measure each stage:

```python
# Each stage should produce a span with timing
with tracer.start_as_current_span("rag.embed_query") as span:
    start = time.time()
    vector = embed(question)
    span.set_attribute("duration_ms", (time.time() - start) * 1000)

with tracer.start_as_current_span("rag.vector_search"):
    chunks = vector_db.search(vector)

# TTFT is measured in the streaming response handler
```

## Identifying The Bottleneck

Run the system at different load levels and capture the waterfall at each:

| Load Level | Dominant Stage | Signal |
|---|---|---|
| Low (5 concurrent) | Model generation (expected) | Long generation span, short queue wait |
| Medium (20 concurrent) | Prefill + queue | Queue wait growing, prefill unchanged |
| High (50 concurrent) | Queue wait | Queue depth rising, TTFT exploding |
| Very high | RAG embedding (if embedding is shared) | Embedding span growing under load |

The bottleneck changes as load increases. A system that looks model-bound at low concurrency may become queue-bound at high concurrency.
