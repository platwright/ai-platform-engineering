# Chapter 01 - AI Cost Visibility

## The Opacity Problem

Unlike most cloud infrastructure costs — where you pay for VMs, storage, or data transfer — AI costs are granular and request-level. A team can run 10 million requests a day and not know their cost until the monthly bill arrives.

Three structural issues create AI cost opacity:

1. **Token-level billing is not intuitive**: "we send 1,000 requests/day" gives no cost estimate without knowing the token counts
2. **Mixed cost sources**: the full cost includes model API fees, embedding service calls, vector database queries, serving infrastructure, and egress — teams typically see only the model API line
3. **No per-request attribution by default**: hosted API invoices show monthly total by model, not by team or product feature

## What Cost Visibility Requires

**Per-request cost tracking**: every model call must log the token usage and the cost it represents, with attribution to the tenant and the use case.

```python
def log_request_cost(tenant: str, model: str, prompt_tokens: int, completion_tokens: int):
    cost = compute_cost(model, prompt_tokens, completion_tokens)
    cost_counter.labels(tenant=tenant, model=model).inc(cost)
    logger.info({
        "event": "model_invocation_cost",
        "tenant": tenant,
        "model": model,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "cost_usd": cost
    })
```

**Aggregated dashboards**: per-request data aggregated into daily, weekly, and monthly views by tenant and model tier.

**Anomaly detection**: alerts when cost rate increases unexpectedly, before the end-of-month invoice.

## Full Cost Inventory

The model API fee is not the full picture. A complete AI cost inventory includes:

| Cost Component | Billing Model | Notes |
|---|---|---|
| Model inference (hosted) | Per token | Input and output tokens billed separately |
| Embedding service (hosted) | Per token or per call | Charged per document ingest and per query |
| Vector database (managed) | Per storage GB + queries | Reads and writes |
| GPU instances (self-hosted) | Per instance-hour | Fixed + overhead, regardless of utilization |
| Networking and egress | Per GB | Data transfer from provider to your infra |
| Evaluation model calls | Per token | Running eval judge incurs inference cost |

Many teams optimize model API cost while paying 2–3× more in embedding and vector DB costs without realizing it.

## Cost Rate vs Total Cost

Two different visibility lenses are useful:

- **Total monthly cost**: useful for budgeting and billing
- **Cost rate (cost per hour or per day)**: useful for detecting anomalies and trends

```promql
# Cost rate: dollars per hour (from Prometheus)
sum(rate(llm_cost_usd_total[1h])) * 3600

# Cost by tenant over last 24 hours
increase(llm_cost_usd_total[24h]) by (tenant)
```

A cost spike visible in the hourly rate can be caught within hours. The same spike hidden in a monthly total may not be noticed for weeks.

## Cost Alerting

Set up alerting before costs exceed budgets:

```yaml
# Alert when hourly cost rate exceeds threshold
- alert: AICostRateHigh
  expr: sum(rate(llm_cost_usd_total[1h])) * 3600 > 10.0  # $10/hour
  for: 15m
  annotations:
    summary: "AI platform cost rate exceeds $10/hour"
    runbook: "https://wiki/runbooks/ai-cost-spike"
```

Budget alerts are more valuable than budget reports. They intervene before overspend rather than reporting it afterward.
