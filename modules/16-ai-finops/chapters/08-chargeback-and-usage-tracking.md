# Chapter 08 - Chargeback and Usage Tracking

## Showback vs Chargeback

**Showback**: show teams their AI usage and cost, for awareness. No financial consequences.

**Chargeback**: bill teams for their AI usage. Real financial consequences — deducted from their budget or recharged to their cost center.

Start with showback. Teams that have never seen their AI cost are often surprised and take action without any financial pressure. Chargeback introduces organizational complexity and requires mature attribution data to be fair.

## The Showback Report

A useful showback report answers for each team:

1. How many tokens did we consume last month?
2. What did that cost?
3. How does our cost compare to other teams?
4. What was our most expensive feature?
5. How has our cost trended over the last 3 months?

```python
def generate_showback_report(month: str) -> dict:
    data = aggregate_usage(month)
    return {
        "month": month,
        "by_tenant": {
            tenant: {
                "prompt_tokens": data[tenant]["prompt_tokens"],
                "completion_tokens": data[tenant]["completion_tokens"],
                "total_tokens": data[tenant]["total_tokens"],
                "cost_usd": data[tenant]["cost_usd"],
                "top_features": data[tenant]["by_feature"][:3],
                "trend_vs_prior_month": compute_trend(tenant, month)
            }
            for tenant in data
        },
        "platform_total_cost_usd": sum(d["cost_usd"] for d in data.values())
    }
```

## Chargeback Models

### Usage-Based Chargeback

Teams are charged exactly for what they use:

```
team-a charge = team-a tokens × provider rate
```

Pros: fair, aligned with actual cost
Cons: unpredictable month-to-month, teams may under-invest in quality to save cost

### Subscription-Based Chargeback

Teams pay a flat monthly fee for a usage tier:

| Tier | Monthly Token Quota | Price |
|---|---|---|
| Starter | 5M tokens | $50/month |
| Standard | 50M tokens | $350/month |
| Growth | 200M tokens | $1,200/month |

Pros: predictable, encourages teams to use AI features without cost fear
Cons: cross-subsidization between high and low users, harder to recover true platform cost

### Cost-Plus Chargeback

Teams pay usage at cost plus a platform overhead percentage:

```
team-a charge = team-a_usage_cost × (1 + platform_overhead)
```

Typical platform overhead: 15–30% to cover shared infrastructure, operations, and evaluation tooling.

## Unit Economics

Unit economics connects AI cost to business metrics:

```python
unit_economics = {
    "cost_per_session": total_cost / total_sessions,
    "cost_per_active_user": total_cost / active_users,
    "cost_per_successful_query": total_cost / successful_queries,
    "ai_cost_as_pct_of_revenue": total_cost / monthly_revenue * 100
}
```

When cost per session is $0.05 and each session generates $2.00 of business value, AI cost is 2.5% of value — clearly justified. When cost per session is $0.50 and the business value is unclear, AI cost needs scrutiny.

## FinOps Review Cadence

| Review Type | Frequency | Participants | Output |
|---|---|---|---|
| Cost anomaly review | Daily (automated) | Platform team | Alert triage |
| Team showback | Monthly | Platform + team leads | Awareness, action items |
| Optimization review | Quarterly | Platform team | Cost reduction initiatives |
| Chargeback reconciliation | Monthly | Platform + Finance | Actual billing |
| Annual FinOps planning | Annual | Engineering leadership | Budget and capacity plan |

## Cost Attribution Maturity Model

Teams progress through stages of AI FinOps maturity:

1. **Blind**: no per-request tracking, monthly invoice is the only signal
2. **Visible**: per-request logging with tenant attribution, monthly reports
3. **Actionable**: real-time dashboards, cost anomaly alerts, team showback
4. **Optimized**: tiered routing, caching, environment controls, regular optimization reviews
5. **Governed**: chargeback in place, budget enforcement, unit economics tracked

Most platforms should aim for Stage 3 (Actionable) before worrying about Stage 4 (Optimized) or Stage 5 (Governed). Optimizing costs you cannot see produces unreliable results.
