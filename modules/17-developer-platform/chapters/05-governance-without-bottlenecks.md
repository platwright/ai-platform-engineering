# Chapter 05 - Governance Without Bottlenecks

## The Governance Paradox

Organizations build AI platforms to accelerate developer velocity. Then they add approval processes to manage risk. The approvals become a bottleneck. Developer velocity drops. Teams work around the platform. The platform loses adoption.

The solution is not to abandon governance — real risks require real controls. The solution is to move governance earlier in the process so it does not block the fast path.

## Two Governance Models

### Approval-Gate Governance

```
Developer proposes → platform team reviews → platform team approves → developer proceeds
```

This model is safe when applied correctly but does not scale. Each approval consumes platform team time. At 5 teams, manageable. At 50 teams, impossible.

### Template-Gate Governance

```
Developer uses approved template → template encodes compliance → developer proceeds
Policy: compliant by construction, not by review
```

The compliance check happened when the template was built and reviewed — once, by the platform team — rather than on every use. Each deployment using the template is compliant without requiring any platform team intervention.

## What Belongs In Templates

Templates enforce governance through the artifacts they produce:

| Governance Requirement | Template Mechanism |
|---|---|
| Prompt version must be tracked | Template includes prompts/ directory with versioning structure |
| Applications must have CI eval gates | Template includes .github/workflows/eval.yml |
| Secrets must not be in code | Template uses environment variable references, not inline secrets |
| Applications must log token usage | Template includes instrumented model call wrapper |
| Applications must have a runbook | Template includes docs/runbook.md to fill in |
| Applications must declare their tenant | Template requires tenantName as a parameter |

A team that uses the template gets all of this automatically. A team that bypasses the template must implement it themselves and prove compliance — which is deliberately higher friction.

## Guardrails vs Paved Roads

Two complementary governance tools:

**Paved road**: the easy path that produces compliant results (golden path templates, pre-approved configurations, default settings that meet requirements)

**Guardrail**: an automated check that flags or blocks non-compliant behavior (CI lint that rejects secrets in config files, gateway policy that enforces rate limits, Kubernetes admission webhook that requires resource limits)

The paved road makes compliance easy. The guardrail catches teams that stray off the path. Together they reduce the need for manual review.

## Asynchronous vs Synchronous Review

When manual review is genuinely needed, make it asynchronous:

- The developer submits their request and continues other work
- The platform team reviews at their own pace
- A maximum response time SLA (e.g., 48 hours) keeps it from becoming a bottleneck
- Clear criteria define what requires review vs what is automatically approved

Reserve synchronous review (real-time meetings, immediate blocking approvals) for:
- novel capabilities not covered by any existing template
- requests to increase resource quotas significantly
- security or compliance exceptions

## The Governance Exception Process

Some teams will legitimately need to deviate from golden paths. An exception process should be:

- **Lightweight**: one form, not a committee
- **Time-bounded**: maximum 3 business days to a decision
- **Transparent**: the criteria for approval are public
- **Auditable**: every exception is recorded
- **Expiring**: exceptions should expire and require periodic renewal

An exception process that is too burdensome drives teams to avoid asking and just deviate silently. Design exceptions to be easy enough that teams use them rather than workarounds.
