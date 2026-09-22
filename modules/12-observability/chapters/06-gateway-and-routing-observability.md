# Chapter 06 - Gateway and Routing Observability

## Why Gateway Observability Is A Leverage Point

The AI gateway sits at the intersection of every model request. It is the single best place to capture:

- which model was used for each request
- which routing decision was made and why
- whether fallback triggered and why
- which tenant generated how much traffic and cost
- whether rate limits are being approached or exceeded

Gateway observability is the foundation of multi-tenant AI platform operations. Without it, operators cannot answer basic questions like "why did response quality drop for team-b this afternoon?" or "which tenant is consuming 40% of our model capacity?"

## Route Selection Logging

Every request handled by the gateway should log the routing decision:

```json
{
  "event": "route_selected",
  "timestamp": "2025-09-01T14:32:10Z",
  "request_id": "req-456",
  "tenant": "team-a",
  "requested_model": "default",
  "selected_model": "gpt-4o-mini-2024-07-18",
  "selected_provider": "openai",
  "routing_reason": "cost_optimized",
  "prompt_tokens_estimated": 843
}
```

Routing reasons should be an enumerated set — not free text — so they are aggregatable as metrics:

```
cost_optimized | latency_optimized | privacy_required | fallback | explicit_request
```

## Fallback Event Observability

Fallback events are resilience events, not just errors. They should be tracked as:

```json
{
  "event": "fallback_triggered",
  "timestamp": "2025-09-01T14:32:11Z",
  "request_id": "req-456",
  "primary_model": "gpt-4o-mini-2024-07-18",
  "fallback_model": "local-ollama",
  "failure_reason": "upstream_timeout",
  "primary_latency_ms": 5001
}
```

Metrics to track:

```promql
# Fallback rate (fraction of requests that fell back)
rate(gateway_fallback_events_total[5m]) / rate(gateway_requests_total[5m])

# Fallback events by reason
sum by (failure_reason) (rate(gateway_fallback_events_total[1h]))
```

A rising fallback rate is a leading indicator of primary model provider issues. Alert before it reaches the level where users notice.

## Rate Limit Monitoring

Rate limit events are both operational signals and business signals:

```json
{
  "event": "rate_limit_hit",
  "timestamp": "2025-09-01T14:32:15Z",
  "tenant": "team-b",
  "limit_type": "tokens_per_minute",
  "current_usage": 95000,
  "limit": 100000,
  "requests_rejected": 1
}
```

Key metrics:

| Metric | Alert Condition |
|---|---|
| Rate limit hits per tenant | Any tenant consistently at > 80% of limit |
| Rate limit rejections | Any rejected requests (tenant is over limit) |
| Tenant token usage vs quota | Within 20% of quota |

Proactively alerting tenants when they approach limits, rather than waiting for rejections, is a better developer experience.

## Cache Observability

Prompt caching and semantic caching are cost-reduction features. Their effectiveness must be measured:

| Metric | Description |
|---|---|
| `gateway_cache_hits_total{cache_type="prompt"}` | Exact prompt cache hits |
| `gateway_cache_hits_total{cache_type="semantic"}` | Semantic cache hits |
| `gateway_cache_misses_total` | Cache misses |
| `gateway_cache_cost_saved_usd_total` | Estimated cost avoided by caching |
| `gateway_semantic_cache_similarity` | Histogram of similarity scores at hit time |

A semantic cache that saves $2/day is probably not worth its added correctness risk and operational complexity. Measure before investing in sophisticated caching.

## Per-Tenant Usage Dashboard

The gateway is the authoritative source for per-tenant usage data. A tenant usage row in the dashboard should show:

- requests per minute (current and 24h trend)
- prompt tokens and completion tokens (hourly rate)
- estimated cost (hourly rate)
- error rate
- rate limit proximity (% of quota used)
- TTFT (to verify SLO compliance per tenant)

Per-tenant visibility enables: chargeback reporting, capacity planning per team, early detection of unusual traffic patterns, and SLO compliance verification.

## Policy Enforcement Events

When the gateway enforces a policy (content filter, scope restriction, model access control), log the enforcement event:

```json
{
  "event": "policy_enforcement",
  "timestamp": "2025-09-01T14:32:20Z",
  "tenant": "team-c",
  "policy": "model_access_control",
  "requested_model": "gpt-4o",
  "outcome": "denied",
  "allowed_models": ["gpt-4o-mini"]
}
```

Policy enforcement events are both operational (for debugging) and security events (for audit). They should flow to both the ops dashboard and the security audit log.
