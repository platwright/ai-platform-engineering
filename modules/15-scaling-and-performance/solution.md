# Module 15 Solution

## Expected Latency Decomposition (Sample RAG)

Approximate timings on a typical developer machine using mock providers:

```
embed_query:    30–60ms    (depends on embedding model)
vector_search:  5–20ms     (in-memory search, fast)
rerank:         0–100ms    (if using a real reranker; 0ms for mock)
llm_generate:   200–2000ms (mock: fast; real: depends on model)
─────────────────────────────────────────────
total:          300–2100ms
ttft:           200–400ms  (first token of LLM response)
```

LLM generation dominates. This is expected and is why model serving is the primary scaling target.

## Autoscaling Policy Reference

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-serving-scaler
  namespace: model-serving
spec:
  scaleTargetRef:
    name: vllm-serving
  pollingInterval: 15
  cooldownPeriod: 120
  minReplicaCount: 1
  maxReplicaCount: 5
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.observability:9090
        metricName: vllm_requests_waiting
        query: sum(vllm_num_requests_waiting)
        threshold: "15"
```

Justification for threshold=15: at low concurrency, queue depth 1–5 is normal. Queue depth consistently above 15 indicates the serving tier cannot drain requests fast enough and a new replica is needed.

Cooldown 120 seconds: model loading takes 2–5 minutes. Setting cooldown shorter than model load time causes thrashing (scale up → scale down before new replica is ready → scale up again).

## Scaling Decision Reference

1. **7B model, insufficient throughput → Scale-out**: model fits on one GPU, add replicas for more total throughput
2. **70B model, doesn't fit on A100 80GB → Scale-up**: need tensor parallelism across 2+ GPUs
3. **Cost per inference too high → Scale-out** with cheaper GPUs (e.g., A10G instead of A100 if model fits)
4. **Remote region latency → Scale-out** with geographically distributed replicas

## Benchmark Analysis Reference

When comparing concurrency levels in mock mode, the mock server may not show the non-linear TTFT degradation that real GPU serving shows (because the mock is not memory-constrained). This is a limitation of mock testing — it validates the tooling and analysis workflow but not the actual performance characteristics.

To see real degradation curves, you need:
- A real GPU serving a real model
- Or CPU-based Ollama serving a small model (shows CPU queuing effects, not GPU memory effects)

The analysis approach is the same regardless of hardware. The numbers will differ.

## Load Test Script Reference (Minimal)

```python
import concurrent.futures, time, requests, statistics

ENDPOINT = "http://localhost:8001/v1/chat/completions"
PROMPTS = [
    "What is retrieval freshness?",
    "Explain chunking strategies for RAG.",
    "What operational signals indicate a RAG platform is degrading?",
]

def send_request(prompt: str) -> dict:
    start = time.time()
    r = requests.post(ENDPOINT, json={
        "model": "test",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }, timeout=30)
    return {
        "status": r.status_code,
        "latency_ms": (time.time() - start) * 1000
    }

for concurrency in [1, 5, 10]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(send_request, PROMPTS[i % len(PROMPTS)])
                   for i in range(concurrency * 5)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]
    
    latencies = [r["latency_ms"] for r in results if r["status"] == 200]
    print(f"Concurrency {concurrency}: p50={statistics.median(latencies):.0f}ms "
          f"p95={sorted(latencies)[int(len(latencies)*0.95)]:.0f}ms")
```
