# Module 17 Solution

## Catalog YAML Reference

A correctly structured AI Gateway catalog entry:

```yaml
# platform/backstage/catalog/ai-gateway.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ai-gateway
  title: AI Gateway
  description: >
    Unified model endpoint for all Acme AI applications. Provides a single
    /api/chat endpoint with model routing, rate limiting, per-tenant usage
    tracking, fallback, and optional prompt caching.
  annotations:
    backstage.io/techdocs-ref: dir:.
  tags:
    - ai-platform
    - gateway
    - production-ready
    - openai-compatible
  links:
    - url: http://localhost:8080
      title: Local Endpoint (dev)
    - url: https://docs.acme.ai/ai-gateway
      title: Documentation
spec:
  type: service
  lifecycle: production
  owner: group:platform-team
  system: ai-platform
  providesApis:
    - ai-gateway-api-v2
  dependsOn:
    - component:project-01-model-api
```

A complete catalog YAML must have `spec.owner` with the `group:` or `user:` prefix, `spec.lifecycle` (experimental / production / deprecated), and meaningful tags for discoverability.

## Template YAML Reference

Key scaffolder template patterns:

```yaml
# Required fields and validation
parameters:
  - properties:
      appName:
        type: string
        pattern: "^[a-z][a-z0-9-]{2,30}$"
        description: "Lowercase, alphanumeric, hyphens only"
      modelTier:
        type: string
        enum: [standard, premium]
        default: standard
        enumNames: ["Standard (gpt-4o-mini)", "Premium (gpt-4o)"]

# Correct template variable syntax
steps:
  - id: fetch-template
    action: fetch:template
    input:
      values:
        appName: ${{ parameters.appName }}
        # NOT {{ appName }} — must be ${{ parameters.name }}
```

Common template mistakes:
- Using `{{ }}` instead of `${{ }}` for parameter references
- Missing `required:` declarations on parameter groups
- Forgetting to include `catalog-info.yaml` in the skeleton (application never appears in catalog)

## API Stability Reference Answers

1. Minimum deprecation notice for stable endpoint: **12 months** before removal
2. HTTP header for deprecation: `Deprecation: <date>` with `Sunset: <removal-date>`
3. Fully sunsetted endpoint response: **410 Gone** (not 404, which implies the resource never existed)

## Team Topologies Matching Reference

1. Platform engineer pair-programming with app team → **Facilitating mode**
2. Team creates service via template with no platform team interaction → **X-as-a-Service mode**
3. Two teams co-designing an API for 3 months → **Collaboration mode**

## Governance Policy Reference

A common mistake: writing governance rules that say "teams should not..." without specifying what happens if they do. Effective governance is enforced (by automation where possible) and has clear consequences when violated.

The most effective governance for AI platforms:
1. Template compliance (automated — the template produces compliant artifacts by construction)
2. Eval gate in CI (automated — pipeline blocks deployments without eval pass)
3. Secret scanning (automated — CI rejects secrets in config files)
4. Quota enforcement (automated — gateway rejects requests over quota)
5. Exception registry (manual but lightweight — one-line request, 48-hour response SLA)

Manual reviews that block the critical path should be reserved for genuinely novel situations that no automation can handle.
