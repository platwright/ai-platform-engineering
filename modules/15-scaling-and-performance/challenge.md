# Module 15 Challenge

## Challenge 1 - Latency Waterfall Analysis

Instrument the sample-rag application to produce a complete latency waterfall for each query.

Add timing measurements to each stage (embed_query, vector_search, rerank, llm_call) and produce output like:

```
query: "What is retrieval freshness?"
  embed_query:    45ms
  vector_search:  18ms
  rerank:         92ms
  llm_generate:   1,647ms
  ──────────────────────
  total:          1,802ms
  ttft:           385ms
```

Run 10 queries and compute p50, p95, p99 for each stage across the 10 runs.

## Challenge 2 - KEDA Autoscaling Manifest

Write a complete KEDA ScaledObject manifest for the model serving deployment that:

1. Scales from 1 to 5 replicas
2. Uses `vllm_num_requests_waiting` as the scaling metric
3. Scales up when queue depth exceeds 15
4. Has a 120-second cooldown before scaling down
5. Includes a ScaledObject and the required TriggerAuthentication/SecretTargetRef if Prometheus requires auth

Also write the Prometheus PrometheusRule that would alert when the autoscaler is at its maximum replica count and queue depth is still growing (capacity ceiling reached).

## Challenge 3 - Load Test Analysis

Design a load test scenario for the sample-rag application that:

1. Ramps from 1 to 30 concurrent users over 5 minutes
2. Uses a realistic prompt distribution (mix of short, medium, and long questions)
3. Measures TTFT, total latency, and error rate at each concurrency level
4. Identifies the concurrency level where TTFT p95 first exceeds 2,000ms
5. Produces a capacity table matching the format in Chapter 07

Write the load test script in Python using the `concurrent.futures` module. You do not need a GPU to write the script — write it against the mock provider.

## Challenge 4 - Quantization Tradeoff Analysis

Research two quantization levels for the Llama 3.1 8B model (FP16 baseline vs INT4):

1. Estimated VRAM usage at each precision
2. Estimated throughput gain from INT4 vs FP16
3. Typical quality degradation observations from public benchmarks

Write a recommendation: for the Acme AI RAG use case, would you deploy INT4 or FP16? Justify based on the tradeoffs.

## Challenge 5 - Capacity Planning Document

Write a one-page capacity planning document for the Acme AI platform covering:

1. Current serving configuration (1 replica, 8B model)
2. Current measured capacity (requests/minute at TTFT SLO)
3. Expected growth (assume 3× current load in 6 months)
4. Scaling options to meet 3× growth (scale-out vs scale-up, with cost comparison)
5. Recommendation with justification

Use concrete numbers wherever possible, even if they are estimates.
