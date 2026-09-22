# Chapter 03 - Platform APIs and Contracts

## Why Platform APIs Need Stability Discipline

An internal platform API is a contract with every team that uses it. When the platform team changes that contract without notice — removes a field, changes a response format, deprecates an endpoint — they create incidents for every consumer simultaneously.

External product APIs have legal and commercial incentives to maintain stability. Internal platform APIs have no such incentives, which is exactly why platform teams need to apply the same discipline deliberately.

## What Makes A Platform API Different From A Service API

A service API is consumed by a bounded set of known callers, typically other services in the same system. If it changes, the team that owns the service also owns (or closely coordinates with) the callers.

A platform API is consumed by an unknown, growing set of callers across the organization. The platform team does not own the callers. When the API changes, the platform team cannot fix every consumer. The consumers must update themselves, on their own timeline.

This difference changes what API stability means:

| Concern | Service API | Platform API |
|---|---|---|
| Breaking change impact | One team | Every team using the platform |
| Discovery of breaking changes | Easy (team knows callers) | Hard (callers are unknown) |
| Migration support | Can coordinate migration | Must provide migration path and support |
| Versioning urgency | Optional | Essential |

## Semantic Versioning For Platform APIs

Adopt semantic versioning for platform API endpoints:

```
/api/v1/chat           ← stable, broad compatibility guarantee
/api/v2/chat           ← current recommended version
/api/v3/chat           ← beta, breaking changes may still happen
```

Version contract:
- **v1 (stable)**: 12-month deprecation notice before removal; maintained for at least 24 months
- **v2 (current)**: 6-month deprecation notice; minor breaking changes require a new minor version
- **v3 (beta)**: no stability guarantee; teams opt in knowing this

## Deprecation Policy

The deprecation lifecycle for platform APIs:

```
Step 1: Mark the endpoint as deprecated in docs and response headers
        Add: Deprecation: Sat, 01 Jan 2027 00:00:00 GMT
             Sunset: Sat, 01 Jul 2027 00:00:00 GMT

Step 2: Notify all teams using the endpoint (from usage logs)

Step 3: Provide a migration guide: what changed, how to update

Step 4: After the Sunset date, return 410 Gone rather than removing silently
```

## Platform API Contract Elements

A complete API contract includes:

```yaml
# api/contracts/gateway-chat-v2.yaml
endpoint: /api/v2/chat
method: POST
stability: stable
deprecated: false
description: "Unified chat endpoint for all model providers"

request:
  required: [message]
  optional: [provider, model, max_tokens, stream]
  authorization: Bearer token with ai:chat scope

response:
  success: 200 with response and usage fields
  errors:
    - 400: malformed request
    - 401: missing or invalid token
    - 429: rate limit exceeded, includes Retry-After
    - 500: upstream model error, retryable
    - 503: platform capacity exceeded, includes Retry-After

sla:
  availability: 99.5%
  p95_latency_ms: 3000
  error_budget: 216 minutes/month
```

Publish these contracts in the developer portal. Every team that depends on the API should be able to read the contract without contacting the platform team.

## Field-Level Stability

Not all fields in an API response have the same stability:

```json
{
  "response": "...",       // stable — present in all versions
  "usage": {              // stable
    "prompt_tokens": 843,
    "completion_tokens": 142
  },
  "model": "gpt-4o-mini", // stable
  "cached": false,        // stable
  "routing_decision": {   // experimental — may be removed
    "selected_route": "openai-mini",
    "reason": "cost_optimized"
  }
}
```

Mark experimental fields explicitly. Teams that rely on experimental fields accept the risk that they may change.

## API Changelog

Maintain a changelog for each platform API:

```markdown
# AI Gateway API Changelog

## v2.1.0 — 2025-09-01
### Added
- `stream` parameter support for chat endpoint
- `cached` field in response indicating cache hit

## v2.0.0 — 2025-06-01
### Changed (breaking)
- Authentication moved from API key in query param to Bearer header
### Migration guide: see docs/migrating-from-v1.md

## v1.2.0 — 2025-03-01
### Added
- `usage` field in all responses
```

The changelog is the audit trail for API evolution and the primary tool for teams evaluating whether to upgrade.
