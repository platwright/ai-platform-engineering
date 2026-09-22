# Chapter 06 - Regression Detection

## What A Regression Looks Like In An LLM System

In conventional software, a regression is a feature that used to work and now does not. The signal is usually binary: a test passes or fails, a function returns a wrong value, an API returns an unexpected status code.

In LLM systems, regressions are probabilistic and often gradual:

- response quality drops from a mean score of 0.85 to 0.76 over two weeks
- TTFT increases by 40% after a model version update
- a specific category of questions that scored well now scores poorly after a prompt change
- a provider silently updates a model and behavior shifts without any API change

None of these produce a test failure or an exception. They require statistical awareness and deliberate measurement.

## Categories Of Regression

### Quality Regression

The semantic quality of responses degrades. Causes include:

- prompt changes that unintentionally alter behavior
- model version updates by the provider
- retrieval pipeline changes that reduce context quality
- evaluation dataset drift (the dataset no longer represents real usage)

### Latency Regression

Response latency increases beyond the established baseline. Causes include:

- model version updates
- longer prompts (token count growth)
- infrastructure changes
- increased concurrency on shared serving infrastructure

### Cost Regression

Token usage or infrastructure cost increases unexpectedly. Causes include:

- prompt length growth
- output length growth (runaway generation without max_tokens)
- routing changes sending more traffic to expensive models
- caching degradation

### Behavioral Regression

The model starts behaving differently in specific situations: refusing requests it previously handled, changing output format, adding or removing disclaimers. Often caused by provider model updates.

## Detection Strategies

### Baseline Establishment

Before any regression detection is meaningful, you need a baseline. Run the full evaluation suite on your current production configuration and record:

```json
{
  "baseline_date": "2025-09-01",
  "prompt_version": "rag-grounding-v1.4.0",
  "model": "gpt-4o-mini-2024-07-18",
  "pass_rate": 0.87,
  "mean_score": 0.82,
  "p95_latency_ms": 1840,
  "mean_tokens_per_request": 1250
}
```

Every subsequent evaluation compares against this baseline.

### Threshold-Based Detection

Set explicit pass/fail thresholds:

| Metric | Pass Threshold | Warning Threshold |
|---|---|---|
| Pass rate | ≥ 0.80 | 0.75–0.79 |
| Mean composite score | ≥ 0.75 | 0.70–0.74 |
| P95 latency | ≤ 2,500ms | 2,000–2,500ms |
| Mean tokens | ≤ 1,500 | 1,250–1,500 |

Thresholds below warning level trigger an alert. Thresholds below pass level block deployment.

### Statistical Significance

A single eval run can show variance. Before acting on a regression signal, check whether the difference is statistically meaningful.

For pass rate changes, a simple test:

```python
from scipy.stats import chi2_contingency

# Baseline: 174 pass out of 200
# Current:  160 pass out of 200
table = [[174, 26], [160, 40]]
chi2, p, dof, expected = chi2_contingency(table)
# If p < 0.05, the difference is statistically significant
```

Do not block a CI run based on a 1% score change when the sample size is 20 cases. Do block based on a 5% change across 200 cases with p < 0.05.

### Continuous Monitoring

CI-only evaluation misses model drift. Schedule periodic evaluation runs against production:

- daily: lightweight 50-case smoke eval to catch sudden shifts
- weekly: full evaluation suite to catch gradual drift
- on every provider model update notification: full suite focused on behavioral regression

## Silent Model Drift

Hosted model providers sometimes update model weights without changing the model version string, or with only a minor version increment. These updates can silently change model behavior.

Detection strategy:

1. Record a set of "canary prompts" with highly stable expected outputs
2. Run these prompts daily and compare outputs against the recorded baseline using semantic similarity
3. Alert when similarity drops below a threshold

```python
CANARY_CASES = [
    {
        "prompt": "Return exactly: OK",
        "expected": "OK",
        "threshold": 1.0  # exact match for deterministic cases
    },
    {
        "prompt": "In one sentence, what is an embedding?",
        "expected": "A dense numeric vector representation of data.",
        "threshold": 0.85  # semantic similarity threshold
    }
]
```

## Regression Diff Reports

When a regression is detected, provide a diff report that shows which cases changed:

```
REGRESSION DETECTED: rag-grounding-v1.5.0 vs v1.4.0
Overall pass rate: 0.81 → 0.74 (FAIL, threshold: 0.80)

Degraded cases (8 new failures):
  eval-031: "What causes retrieval failure?" 
    Before: score 2.8/3, passed
    After:  score 1.4/3, failed
    Diff: Response no longer mentions index staleness

  eval-076: "Explain chunking strategies"
    Before: score 2.6/3, passed
    After:  score 1.2/3, failed
    Diff: Response became generic, lost platform context
```

This report goes directly to the developer who made the prompt change, enabling targeted diagnosis rather than a blind investigation.

## Rollback Triggers

Define which regression signals trigger automatic versus manual rollback:

| Regression Type | Severity | Response |
|---|---|---|
| Pass rate drops > 10% | Critical | Auto-block deployment |
| Pass rate drops 5–10% | High | Alert + manual review required |
| P95 latency increases > 50% | High | Alert + manual review |
| Cost per request increases > 30% | Medium | Alert, investigate within 24h |
| Behavioral shift in canary prompts | High | Alert + escalate to provider |
