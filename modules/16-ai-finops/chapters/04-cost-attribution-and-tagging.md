# Chapter 04 - Cost Attribution and Tagging

## Why Attribution Comes Before Optimization

You cannot manage what you cannot see. Before optimizing AI costs, you need to know who is spending what. Without per-tenant attribution:

- high-cost features or teams are invisible
- optimization efforts may target low-cost areas and miss the real drivers
- chargeback (billing internal teams) is impossible
- anomalies (runaway cost from one team) are discovered only on the monthly invoice

## The Attribution Model

Every model API call must carry attribution metadata at the time it is made. Retrofitting attribution to existing logs is difficult. Add it from the start.

Required attribution fields:

| Field | Description | Where Set |
|---|---|---|
| `tenant` | Team or organizational unit | Request header or JWT claim |
| `application` | Application name | Application config |
| `feature` | Specific feature or use case | Feature-level code tag |
| `environment` | prod / staging / dev | Environment config |
| `model` | Model name and version | Gateway routing |
| `request_type` | chat / rag / eval / batch | Application code |

## Tagging at the Gateway

The AI gateway is the right layer to capture attribution because all model traffic flows through it:

```python
def handle_chat(request: dict, claims: dict) -> dict:
    tenant = claims["tenant"]
    app = request.get("application", "unknown")
    feature = request.get("feature", "unknown")

    response = call_model(request)
    usage = response["usage"]

    # Record cost with full attribution
    cost = compute_cost(request["model"], usage["prompt_tokens"], usage["completion_tokens"])
    
    cost_counter.labels(
        tenant=tenant,
        application=app,
        feature=feature,
        model=request["model"],
        environment=os.getenv("APP_ENV", "prod")
    ).inc(cost)

    return response
```

## Attribution Hierarchy

A useful attribution hierarchy flows from coarse to fine:

```
Organization
└── Team / Tenant
    └── Application
        └── Feature
            └── Request Type
                └── Model
```

Report at different levels for different audiences:
- **CFO / Budget owner**: organization and team level
- **Engineering lead**: application and feature level
- **Platform team**: model and request type level

## Log-Based Attribution

If you cannot add Prometheus metrics immediately, structured logs are a viable starting point:

```json
{
  "event": "model_call",
  "timestamp": "2025-09-01T14:32:10Z",
  "tenant": "team-a",
  "application": "rag-chat",
  "feature": "knowledge-search",
  "model": "gpt-4o-mini-2024-07-18",
  "prompt_tokens": 2500,
  "completion_tokens": 300,
  "cost_usd": 0.000555,
  "environment": "prod"
}
```

Aggregate daily from logs:

```bash
# Daily cost by tenant from structured logs
cat gateway.log | jq -r '[.tenant, .cost_usd] | @tsv' | \
  awk '{cost[$1]+=$2} END {for(t in cost) print t, cost[t]}' | \
  sort -k2 -rn
```

## Tagging Gaps

Attribution fails when:
- requests arrive without tenant context (anonymous or missing JWT)
- multiple tenants use the same API key (no per-tenant granularity)
- batch jobs are not tagged with a requesting team
- the "feature" field is omitted or inconsistent

Address tagging gaps before building reports. A cost report with 30% "unknown" attribution is not useful.
