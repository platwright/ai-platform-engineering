# Chapter 03 - SLI and SLO Design for AI Systems

## SLI, SLO, and SLA Refresher

- **SLI** (Service Level Indicator): a quantitative measure of service behavior (e.g., request success rate)
- **SLO** (Service Level Objective): a target for an SLI (e.g., 99.5% of requests succeed)
- **SLA** (Service Level Agreement): a contract with consequences for SLO violation (not the same as SLO)
- **Error budget**: the amount of SLO violation allowed before action is required (1 - SLO)

## SLI Categories For AI Systems

AI platforms need SLIs across both reliability dimensions:

### Availability SLIs

```
availability = successful_requests / total_requests

Where "successful" means: HTTP 2xx with a well-formed response
```

### Latency SLIs

```
ttft_sli = count(ttft < threshold) / total_requests
e2e_latency_sli = count(latency < threshold) / total_requests
```

Latency SLIs are usually expressed as a proportion of requests meeting a threshold rather than as a mean, because means hide tail latency.

### Quality SLIs

```
quality_sli = eval_pass_rate  (from scheduled eval runs)
groundedness_sli = mean(groundedness_score)  (from online eval)
```

Quality SLIs are measured by evaluation pipelines, not by request counters.

### Retrieval SLIs

```
retrieval_success_sli = count(chunks_returned > 0) / total_rag_queries
freshness_sli = count(index_age < threshold) / total_tenants_checked
```

## Designing SLOs

### Availability SLO

Start with a target that reflects real user expectations, not aspirational perfection:

| Service Type | Typical Production Target |
|---|---|
| Interactive chat | 99.5% (43 minutes downtime per month) |
| RAG query | 99.5% |
| Batch evaluation | 99% |
| Agent platform | 99.5% |

99.9% is a popular target but has an error budget of only 43 minutes per month — very little room for deployments, incidents, or planned maintenance.

### Latency SLO

Express as a proportion-at-threshold, with separate SLOs for TTFT and end-to-end latency:

```
SLO: 95% of requests have TTFT < 800ms
SLO: 99% of requests complete within 5,000ms
```

Set thresholds based on measured baselines. A threshold set lower than the measured p95 will constantly burn your error budget.

### Quality SLO

```
SLO: 7-day rolling eval pass rate >= 0.80
SLO: Online eval groundedness score >= 2.5/3.0 on weekly sample
```

Quality SLOs need a baseline eval run and a burn-rate alerting strategy, because a single eval below threshold may be measurement noise.

## Error Budget Calculation

```
Error budget = (1 - SLO) × time_period

Example: 99.5% availability SLO over 30 days
Error budget = 0.005 × 30 × 24 × 60 = 216 minutes per month

If a deployment window takes 15 minutes of degraded availability,
that costs 15 / 216 = 6.9% of the monthly error budget.
```

## Error Budget Policy

Define what happens at different burn rates:

| Budget Remaining | Policy |
|---|---|
| > 50% | Normal operations, deployments proceed as planned |
| 25–50% | Review pending deployments for risk, increase post-deploy monitoring |
| < 25% | High-risk deployments require additional sign-off |
| < 10% | Feature deployments paused; reliability work prioritized |
| 0% | Incident declared, all changes frozen, escalation required |

## Quality Error Budget

Apply the same logic to quality SLOs:

```
Quality budget = (1 - 0.80) × 7 days = 1.4 days worth of below-SLO scores

If the eval score is 0.72 for two consecutive daily runs,
that consumes: 2 / 1.4 ≈ 143% of the weekly budget → incident
```

## Common SLO Design Mistakes

### Setting SLOs Without Baselines

An SLO of 99.9% availability when your measured baseline is 99.6% means your error budget is exhausted from day one. Measure first, set SLO second.

### Separate SLOs That Conflict

If availability SLO says 99.5% and the fallback path has 10% quality degradation, activating fallback to protect availability may push quality SLO into violation. Design SLOs that are coherent with each other.

### Ignoring The Quality Dimension Entirely

Teams that only define technical SLOs may hit their availability and latency targets while experiencing persistent quality degradation. Monitor both dimensions from the start.

### Too Many SLOs

Start with 3–5 SLOs covering the most user-visible concerns. More SLOs create more alert noise without proportionally more signal. Add SLOs as the platform matures and specific reliability gaps emerge.
