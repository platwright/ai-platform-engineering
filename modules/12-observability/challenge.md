# Module 12 Challenge

## Challenge 1 - End-to-End Instrumentation

Extend the `applications/sample-rag/app.py` to use the `prometheus_client` library and expose a `/metrics` endpoint.

Install the library:
```bash
pip install prometheus-client
```

Implement at minimum:
- `rag_query_total` counter with `tenant` and `status` labels
- `rag_query_duration_seconds` histogram
- `rag_llm_tokens_total` counter with `tenant` and `type` labels (`prompt` / `completion`)

Verify the metrics are exposed:
```bash
python applications/sample-rag/app.py serve &
curl http://localhost:8090/metrics  # or whatever port your app exposes
```

## Challenge 2 - Distributed Trace Simulation

Without requiring a real OTel Collector, simulate distributed trace logging by producing structured log entries that contain:

- a `trace_id` (generate a UUID at the start of each request)
- a `span_id` and `parent_span_id` for each logical step
- start and end timestamps for each step
- the standard GenAI span attributes for the LLM call

Write a Python function `create_span(name, parent_span_id, attributes)` that produces a structured span log entry, and use it to instrument one full RAG query.

The output should show a span tree like:

```json
{"name": "rag.handle_query", "trace_id": "...", "span_id": "a1", "parent": null, "start_ms": 0, "end_ms": 1833}
{"name": "rag.embed_query",  "trace_id": "...", "span_id": "a2", "parent": "a1", "start_ms": 0, "end_ms": 45}
{"name": "rag.vector_search","trace_id": "...", "span_id": "a3", "parent": "a1", "start_ms": 46, "end_ms": 64}
{"name": "llm.generate",     "trace_id": "...", "span_id": "a4", "parent": "a1", "start_ms": 65, "end_ms": 1833,
 "gen_ai.usage.prompt_tokens": 843, "gen_ai.usage.completion_tokens": 142}
```

## Challenge 3 - Dashboard JSON Design

Write a Grafana dashboard JSON definition (or a structured YAML equivalent) for a 3-panel platform overview row:

1. **Request rate** (time series): `rate(rag_query_total[5m])` by tenant
2. **TTFT p95** (stat panel with threshold coloring): `histogram_quantile(0.95, rate(llm_time_to_first_token_seconds_bucket[5m]))`
3. **Cost per hour** (stat panel): `increase(llm_cost_usd_total[1h])`

Each panel should specify the Prometheus query, the visualization type, and the threshold values for color-coding.

## Challenge 4 - Alert Fatigue Analysis

The Acme AI platform team has 24 alerts configured. In the last week, 6 of them fired more than 20 times each. Review the following alert conditions and identify which ones are likely to produce noise rather than actionable signal:

1. `gpu_utilization > 80%` — fires immediately with no duration requirement
2. `llm_request_errors > 0` — any error at all
3. `kv_cache_utilization > 90%` for 2 minutes
4. `eval_score < 0.85` with no duration requirement (fires after every eval run where score is between 0.75 and 0.85)
5. `rag_query_total rate == 0` for 1 minute during business hours

For each alert, explain whether it is well-designed or not, and suggest an improved version.

## Challenge 5 - Quality SLO Definition

Define three quality SLOs for the Acme AI RAG platform:

For each SLO:
1. Write the SLI definition (what is being measured and how)
2. Write the SLO target (the threshold)
3. Describe how you would measure compliance on a daily basis
4. Describe what breach of the SLO should trigger operationally
5. Identify the single metric most likely to provide an early warning before breach
