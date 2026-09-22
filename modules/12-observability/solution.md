# Module 12 Solution

## Expected Token Logging Output

After adding structured logging to the RAG query path, a successful query should produce a log line similar to:

```json
{
  "timestamp": "2025-09-01T14:32:10Z",
  "question_length_chars": 32,
  "prompt_tokens": 843,
  "completion_tokens": 142,
  "total_tokens": 985,
  "latency_ms": 1834.5
}
```

If `prompt_tokens` is 0 or absent, the upstream model response is not returning usage metadata. The mock providers in Project 01 return simulated usage data. If you are testing against a real provider, check that the response includes the `usage` field.

## Alert Design Reference

Alert for TTFT exceeding 2 seconds at p95:

```yaml
groups:
  - name: rag_platform
    rules:
      - alert: RAGHighTTFT
        expr: |
          histogram_quantile(0.95,
            rate(rag_query_duration_seconds_bucket[5m])
          ) > 2.0
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "RAG query p95 latency above 2s"
          description: "p95 latency is {{ $value }}s"
          runbook: "https://wiki/runbooks/rag-high-latency"
```

The `for: 5m` clause prevents false alerts from brief spikes. The 2-second threshold is appropriate when the expected nominal p95 is 1.2–1.5 seconds.

## Alert Fatigue Analysis Reference

1. `gpu_utilization > 80%` — **noisy**: GPUs routinely hit 80%+ during normal serving. Add `for: 10m` and raise to 95%.
2. `llm_request_errors > 0` — **very noisy**: any single error fires the alert. Use a rate: `rate(errors[5m]) / rate(total[5m]) > 0.05`.
3. `kv_cache_utilization > 90%` for 2 minutes — **reasonable**: sustained high cache utilization is actionable. Keep this.
4. `eval_score < 0.85` with no duration — **contextually noisy**: fires on every eval run between 0.75 and 0.85. Use `< 0.75` as the alert threshold, with `< 0.80` as a warning.
5. `rag_query_total rate == 0` for 1 minute — **potentially valid** but too short. Extend to 5 minutes to avoid false alerts from brief quiet periods.

## Observability Design Reference (Minimal Set)

The highest-value metrics to add to the RAG application first:

1. `rag_query_total` (counter) — with tenant and status labels. Enables request rate and error rate calculation.
2. `rag_query_duration_seconds` (histogram) — TTFT or total latency depending on implementation. Enables latency SLO alerting.
3. `rag_llm_tokens_total` (counter) — with tenant label. Enables cost attribution.
4. `rag_zero_results_total` (counter) — queries returning no chunks. Low cost signal, high diagnostic value.

These four metrics, plus the existing HTTP metrics from the serving layer, cover the core operational surface with minimal implementation effort.

## Quality SLO Reference Design

**SLO 1: Answer Quality**
- SLI: daily offline eval pass rate on `rag-eval-v3.1.json`
- Target: ≥ 0.80 over any 7-day rolling window
- Measurement: daily scheduled eval job writing score to `ai_platform_eval_score`
- Breach response: investigate prompt or model changes from the last 7 days, compare to baseline
- Early warning: online eval groundedness score dropping below 2.0/3.0

**SLO 2: Retrieval Freshness**
- SLI: maximum age of any tenant's RAG index in hours
- Target: no tenant's index older than 24 hours
- Measurement: `rag_index_last_updated_timestamp` gauge per tenant
- Breach response: trigger manual re-ingestion, investigate ingestion job failures
- Early warning: index age approaching 20 hours

**SLO 3: Response Latency**
- SLI: p95 end-to-end query latency
- Target: ≤ 3.0 seconds at p95 over any 5-minute window
- Measurement: `histogram_quantile(0.95, rate(rag_query_duration_seconds_bucket[5m]))`
- Breach response: check queue depth, KV cache, prompt token length trends
- Early warning: p95 latency crossing 2.0 seconds
