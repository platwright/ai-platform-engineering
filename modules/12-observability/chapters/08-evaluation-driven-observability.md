# Chapter 08 - Evaluation-Driven Observability

## The Gap That Runtime Telemetry Cannot Fill

Runtime observability answers: is the system up, fast, and free of errors?

It cannot answer: is the system producing correct, relevant, and safe responses?

A platform can have 99.9% uptime, sub-second TTFT, and zero HTTP errors while simultaneously returning hallucinated facts, missing the point of half of user queries, and occasionally producing inappropriate content. None of these quality failures show up in a Prometheus dashboard.

Evaluation-driven observability closes this gap by treating quality measurement as a continuous operational concern, not a one-time pre-launch check.

## Online Evaluation

Online evaluation scores a sample of live production traffic in real time.

```
Production Traffic
        │
        ├─── 100% → serve response to user
        │
        └─── 5% random sample → evaluation pipeline
                        │
                        ▼
                   Eval Scorer
                 (LLM-as-judge or rubric)
                        │
                        ▼
              Quality Score Time-Series
```

The evaluation pipeline:
1. Captures the request, response, and retrieved context
2. Sends to an async eval worker (does not block the user request)
3. Scores the response against a rubric
4. Writes the score to a time-series metric

Practical considerations:
- sample rate must be high enough for statistical significance but low enough to keep eval costs reasonable
- the eval worker must not create backpressure on the serving path
- scores are approximate — online eval uses simpler rubrics than offline eval

## Offline Scheduled Evaluation

Scheduled eval jobs run the full evaluation suite against the current production configuration on a cadence (daily, weekly, or after each deployment):

```bash
# Scheduled job (cron or CI)
python eval/run_eval.py \
  --dataset eval/datasets/rag-eval-v3.1.json \
  --mode production \
  --output eval/runs/$(date +%Y%m%d).json
```

The output is written to a metric:

```python
eval_score_gauge = Gauge("ai_platform_eval_score", "Latest eval pass rate", ["dataset_version"])
eval_score_gauge.labels(dataset_version="v3.1").set(run_result["pass_rate"])
```

This metric appears on the platform dashboard as a 7-day trend, providing a quality signal that spans individual request measurements.

## Quality SLO Definition

Evaluation scores can be formalized as SLOs:

| SLO | Measurement | Target |
|---|---|---|
| RAG answer quality | Daily offline eval pass rate | ≥ 0.80 |
| Chat response quality | Weekly offline eval pass rate | ≥ 0.82 |
| RAG groundedness | Online eval: groundedness score | ≥ 2.5 / 3.0 |

Quality SLOs behave differently from latency SLOs:
- they change when prompts, models, or retrieval pipelines change
- they require baseline re-establishment after major system changes
- they are more expensive to measure than latency (eval costs money)

## Connecting Eval Scores To Incidents

When an eval score drops, the investigation should connect to runtime signals:

```
Eval score drops from 0.88 to 0.74 (detected on daily job)
        │
        ▼
Was there a prompt version change? → check prompt registry
Was there a model update? → check model version in recent traces
Did retrieval quality change? → check RAG staleness and reranker scores
Did input distribution change? → check prompt token length trends
```

This investigation path is only possible when runtime metrics, traces, and eval scores share a common time axis and can be correlated.

## Evaluation As A Dashboard Row

On the platform overview dashboard, the quality row sits alongside the reliability and cost rows:

```
Quality Row:
  ├── Latest eval score: 0.82 (↑ from 0.79 last week)
  ├── 7-day eval score trend [sparkline]
  ├── Negative user feedback rate: 3.2%
  └── Low-confidence responses (online eval): 8.4%
```

When the quality row and the reliability row tell different stories — the platform is fast and available but eval scores are dropping — that is the scenario where evaluation-driven observability provides value that runtime monitoring alone cannot.

## Practical Starting Point

Organizations new to evaluation-driven observability should start with:

1. **Daily offline eval job** on the top 20-30 eval cases. Publish the score to a Grafana metric. Low cost, high value.
2. **Negative feedback rate metric** from the application. Cheap to collect, early warning signal.
3. **Zero-result RAG query rate**. Detects retrieval failure without expensive eval.
4. **Canary prompt daily check** (from Module 11). Detects silent model drift.

Add online evaluation and full quality SLO tracking as the platform and the eval dataset mature.
