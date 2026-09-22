# Chapter 03 - Scaling the AI Gateway

## Gateway Scaling Characteristics

The AI gateway is a proxy layer with CPU and memory requirements determined by:
- request and response processing (JSON parsing, header manipulation, routing logic)
- in-flight connection count (depends on downstream latency and concurrency)
- semantic cache lookup (if enabled)
- rate limiting state (per-tenant token counts)

The gateway is typically not the bottleneck in AI systems, but it can become one if it buffers responses rather than streaming them, or if semantic cache operations are slow.

## Gateway Horizontal Scaling

Gateway pods are stateless if rate limiting uses an external store (Redis) rather than in-process memory. Stateless gateways scale horizontally without coordination:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-gateway
spec:
  replicas: 3  # Start with 3 for HA; autoscale based on CPU
  template:
    spec:
      containers:
        - name: gateway
          resources:
            requests:
              cpu: "500m"
              memory: "512Mi"
            limits:
              cpu: "2"
              memory: "2Gi"
```

If rate limiting state is in-process (a Python dict), each replica has independent counters and rate limits are not enforced consistently across replicas. Move rate limit state to Redis before scaling horizontally.

## Streaming Pass-Through vs Buffering

A gateway that buffers the full model response before returning it to the client doubles the effective latency from the user's perspective:

```
Without buffering: user sees first token at TTFT = 400ms
With buffering: user sees first token when full response is complete = 400ms + generation_time
```

Configure the gateway to pass through streaming responses without buffering:

```python
# WRONG: buffers entire response
response_text = call_upstream_and_wait()
return response_text

# RIGHT: stream directly to client
def stream_response(upstream_response):
    for chunk in upstream_response.iter_content():
        yield chunk
```

The gateway can still capture the full response for logging by teeing the stream to an async buffer.

## Connection Multiplexing

Each gateway replica maintains persistent HTTP connections to each model server replica. At high concurrency, connection management becomes important:

- Use HTTP/2 for upstream connections to model servers where supported (multiplexes many requests over fewer TCP connections)
- Set keep-alive on HTTP/1.1 connections to avoid TCP handshake overhead per request
- Limit the number of connections per upstream to avoid overwhelming a single server instance

## Semantic Cache Scaling

Semantic cache (approximate match for similar queries) requires an embedding lookup on every request. At scale, the embedding service becomes the bottleneck if the semantic cache is enabled:

- Batching embedding requests for multiple concurrent cache lookups reduces per-lookup cost
- Consider whether semantic cache hit rate justifies the embedding cost and latency overhead
- A 15% hit rate with 50ms embedding overhead saves money but adds latency to 85% of requests

Measure before enabling semantic caching at scale. For many platforms, a simple exact-match prompt cache (checking the hash of the full prompt) provides most of the benefit at much lower overhead.

## Gateway Observability For Scaling Decisions

Key metrics for gateway scaling decisions:

```promql
# Gateway CPU utilization (scale up gateway if approaching limits)
rate(container_cpu_usage_seconds_total{container="ai-gateway"}[5m])

# In-flight connections to model servers
gateway_upstream_connections_active

# Cache lookup latency (if semantic cache enabled)
histogram_quantile(0.95, rate(gateway_cache_lookup_duration_seconds_bucket[5m]))
```
