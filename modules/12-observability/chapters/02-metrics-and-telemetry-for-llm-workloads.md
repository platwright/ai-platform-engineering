# Chapter 02 - Metrics and Telemetry for LLM Workloads

## What Makes LLM Metrics Different

Conventional web service metrics are well-understood: request rate, error rate, latency percentiles, saturation. These still apply to LLM workloads. What changes is that the operational behavior of LLM services is governed by token dynamics that conventional metrics do not capture.

Two requests with identical HTTP response time can have radically different cost profiles if one generated 50 tokens and the other generated 800. Two requests with identical token counts can have very different user experience if one had TTFT of 200ms and the other had TTFT of 2,000ms.

Effective LLM monitoring requires metrics designed for these token-centric dynamics.

## Request-Level Metrics

These are recorded per inference request:

| Metric | Type | Description |
|---|---|---|
| `llm_request_total` | Counter | Total requests, labeled by model and status |
| `llm_request_errors_total` | Counter | Error count by error type |
| `llm_request_duration_seconds` | Histogram | End-to-end request duration |
| `llm_time_to_first_token_seconds` | Histogram | TTFT distribution |
| `llm_prompt_tokens_total` | Counter | Cumulative prompt tokens by model and tenant |
| `llm_completion_tokens_total` | Counter | Cumulative completion tokens by model and tenant |
| `llm_cost_usd_total` | Counter | Cumulative estimated cost by model and tenant |

## Model Serving Metrics

These are recorded at the serving layer (vLLM, TGI, or similar):

| Metric | Description |
|---|---|
| `vllm_num_requests_running` | Active requests currently being processed |
| `vllm_num_requests_waiting` | Requests waiting in the queue |
| `vllm_gpu_cache_usage_perc` | KV cache utilization percentage |
| `vllm_generation_tokens_per_second` | Output tokens generated per second |
| `vllm_time_to_first_token_seconds` | TTFT as measured at the server |

vLLM exposes these natively through a Prometheus `/metrics` endpoint. For other serving backends, check the documentation for the metrics endpoint format.

## Gateway Metrics

| Metric | Description |
|---|---|
| `gateway_requests_total` | Requests by tenant, model, and route |
| `gateway_route_selections_total` | Which route was selected per request |
| `gateway_fallback_events_total` | Fallback activations and reasons |
| `gateway_rate_limit_events_total` | Rate limit hits by tenant |
| `gateway_cache_hits_total` | Prompt and semantic cache hit counts |
| `gateway_cache_misses_total` | Cache miss counts |

## Infrastructure Metrics For GPU Serving

| Metric | Source | Description |
|---|---|---|
| `DCGM_FI_DEV_GPU_UTIL` | DCGM exporter | GPU utilization percentage |
| `DCGM_FI_DEV_FB_USED` | DCGM exporter | GPU memory used (bytes) |
| `DCGM_FI_DEV_FB_FREE` | DCGM exporter | GPU memory free (bytes) |
| `DCGM_FI_DEV_SM_CLOCK` | DCGM exporter | SM clock frequency |
| `DCGM_FI_DEV_GPU_TEMP` | DCGM exporter | GPU temperature |

The NVIDIA DCGM Exporter is the standard Prometheus exporter for GPU metrics in Kubernetes environments.

## Instrumentation Pattern (Python)

A minimal instrumentation pattern that captures the critical signals:

```python
import time
from prometheus_client import Counter, Histogram

request_counter = Counter(
    "llm_request_total",
    "Total LLM requests",
    ["model", "tenant", "status"]
)
ttft_histogram = Histogram(
    "llm_time_to_first_token_seconds",
    "Time to first token",
    ["model"],
    buckets=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
)
token_counter = Counter(
    "llm_tokens_total",
    "Total tokens processed",
    ["model", "tenant", "type"]  # type: prompt or completion
)

def instrumented_llm_call(model: str, tenant: str, messages: list) -> dict:
    start = time.time()
    first_token_time = None

    try:
        response = call_model_api(model=model, messages=messages, stream=True)

        for chunk in response:
            if first_token_time is None:
                first_token_time = time.time()
                ttft_histogram.labels(model=model).observe(first_token_time - start)
            # accumulate content...

        usage = response.usage
        token_counter.labels(model=model, tenant=tenant, type="prompt").inc(usage.prompt_tokens)
        token_counter.labels(model=model, tenant=tenant, type="completion").inc(usage.completion_tokens)
        request_counter.labels(model=model, tenant=tenant, status="success").inc()

        return {"response": ..., "usage": usage}

    except Exception as e:
        request_counter.labels(model=model, tenant=tenant, status="error").inc()
        raise
```

## Cost Rate Metric

Tracking cost as a time-series metric enables cost alerting and trending:

```python
COST_COUNTER = Counter(
    "llm_cost_usd_total",
    "Estimated LLM cost in USD",
    ["model", "tenant"]
)

COST_PER_M_TOKENS = {
    "gpt-4o-mini-2024-07-18": {"prompt": 0.15, "completion": 0.60},
    "gpt-4o-2024-08-06":      {"prompt": 5.00, "completion": 15.00},
}

def record_cost(model: str, tenant: str, prompt_tokens: int, completion_tokens: int):
    rates = COST_PER_M_TOKENS.get(model, {"prompt": 0.0, "completion": 0.0})
    cost = (prompt_tokens * rates["prompt"] + completion_tokens * rates["completion"]) / 1_000_000
    COST_COUNTER.labels(model=model, tenant=tenant).inc(cost)
```

## Key Prometheus Queries

```promql
# Request rate over last 5 minutes
rate(llm_request_total[5m])

# Error rate
rate(llm_request_total{status="error"}[5m]) / rate(llm_request_total[5m])

# TTFT 95th percentile
histogram_quantile(0.95, rate(llm_time_to_first_token_seconds_bucket[5m]))

# Total token cost per hour by tenant
increase(llm_cost_usd_total[1h])

# KV cache utilization
vllm_gpu_cache_usage_perc

# Queue depth
vllm_num_requests_waiting
```
