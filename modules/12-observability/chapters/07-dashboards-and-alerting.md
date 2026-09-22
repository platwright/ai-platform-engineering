# Chapter 07 - Dashboards and Alerting

## Dashboard Design Principles For AI Systems

A good operations dashboard makes the most important information visible in three seconds and supports drill-down for investigation. AI platform dashboards fail when:

- they display too many panels of equal visual weight
- they mix operational signals with research metrics
- they have no hierarchy — everything looks equally important
- they are built once and never updated as the system evolves

Design for two audiences: the on-call operator who needs to detect and diagnose incidents quickly, and the platform lead who needs to track trends over time.

## Platform Overview Dashboard

The top row should answer: "Is the platform healthy right now?"

```
Row 1: Summary panels (30-second read)
  ├─ Total requests/min (current vs 1h ago)
  ├─ Error rate % (with threshold line)
  ├─ TTFT p95 (with SLO threshold line)
  ├─ Active alerts count
  └─ Estimated cost/hr

Row 2: Key time-series
  ├─ Request rate by model (stacked)
  └─ Error rate over time

Row 3: Latency
  ├─ TTFT distribution (heatmap)
  └─ End-to-end latency p50/p95/p99

Row 4: Resource
  ├─ GPU utilization by node
  ├─ KV cache utilization
  └─ Queue depth

Row 5: Quality and Cost
  ├─ Eval score 7-day trend
  └─ Cost rate by tenant (stacked)
```

## Alert Priority Framework

Design alerts with explicit priority levels:

### P1 — Service Down (page immediately)

- Error rate > 10% for more than 2 minutes
- All model serving replicas unreachable
- AI gateway returning 5xx for > 50% of requests

### P2 — Degraded Service (notify, investigate within 30 minutes)

- TTFT p95 > 3× baseline for 5+ minutes
- Queue depth > 50 requests for 5+ minutes
- Any model provider returning > 5% 5xx
- Agent approval bypass event detected

### P3 — Warning Trend (review within business hours)

- Eval score dropping below 0.75
- GPU memory > 90%
- Single tenant consuming > 60% of capacity
- RAG index staleness > 24 hours

### Informational

- Prompt version deployed
- New tenant onboarded
- Model version change detected

## Alert Configuration (Prometheus)

```yaml
groups:
  - name: ai_platform_p1
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(llm_request_total{status="error"}[2m]))
          /
          sum(rate(llm_request_total[2m])) > 0.10
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "LLM error rate above 10%"
          runbook: "https://wiki/runbooks/llm-high-error-rate"

  - name: ai_platform_p2
    rules:
      - alert: TTFTRegression
        expr: |
          histogram_quantile(0.95, rate(llm_time_to_first_token_seconds_bucket[5m]))
          > 3.0
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "TTFT p95 above 3 seconds"
          runbook: "https://wiki/runbooks/ttft-regression"

      - alert: HighQueueDepth
        expr: vllm_num_requests_waiting > 50
        for: 5m
        labels:
          severity: high
        annotations:
          summary: "Model serving queue depth > 50"

  - name: ai_platform_p3
    rules:
      - alert: EvalScoreLow
        expr: ai_platform_eval_score < 0.75
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "Evaluation score below 0.75"

      - alert: RAGIndexStale
        expr: (time() - rag_index_last_updated_timestamp) > 86400
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "RAG index stale for {{ $labels.tenant }}"
```

## Runbook Structure For AI Alerts

Every alert should link to a runbook. AI runbooks need AI-specific diagnostic steps:

```markdown
# Runbook: TTFT Regression

## Symptoms
TTFT p95 > 3 seconds and rising.

## Immediate Checks
1. Check vllm_num_requests_waiting — is the queue growing?
2. Check vllm_gpu_cache_usage_perc — is KV cache over 85%?
3. Check if a new model or configuration was deployed recently.
4. Check if input prompt lengths increased (prompt_tokens histogram).

## Diagnosis Tree
- Queue growing + cache full → scale serving replicas or reduce context length
- Queue growing + cache normal → load spike, check if rate limiting needed
- Queue normal + cache normal → check if model version changed
- Queue normal + high cache → flush or resize KV cache

## Escalation
If TTFT does not recover within 15 minutes, escalate to platform on-call.
```

## Avoiding Alert Fatigue

AI systems introduce new sources of noise:

- non-deterministic outputs cause quality metrics to fluctuate naturally
- GPU metrics have high variance during batch processing
- model provider latency has higher natural variance than typical databases

Mitigate alert fatigue with:

- **Minimum duration**: alert only after the condition persists for N minutes
- **Burn rate alerting**: alert based on the rate of SLO budget consumption, not on instantaneous threshold crossings
- **Business hours routing**: P3 alerts notify during business hours only
- **Deduplication**: suppress repeated alerts for the same condition
