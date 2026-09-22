# Chapter 08 - Incident Response for AI Platforms

## What Makes AI Incidents Different

AI incidents share characteristics with both software incidents (the system is down or throwing errors) and data quality incidents (the outputs are wrong but the system is running). AI incident response must handle both cases, often simultaneously.

The most important difference: **quality incidents produce no error code**. An operator monitoring only error rates and HTTP status codes will not detect a quality incident until users complain. Incident response procedures must include quality signals and have explicit procedures for quality-only failures.

## Incident Severity Levels

Define severity levels that cover both technical and quality dimensions:

| Severity | Technical Trigger | Quality Trigger | Response Time |
|---|---|---|---|
| P1 Critical | All requests failing (> 90% error rate) | System producing harmful outputs | Immediate page |
| P2 High | Error rate > 10%, TTFT > 3× SLO | Eval score < 0.65 (severe quality drop) | 30 minutes |
| P3 Medium | Error rate > 2%, TTFT > 2× SLO | Eval score 0.65–0.75 | 2 hours |
| P4 Low | Error rate > 0.5% sustained | Eval score 0.75–0.80 (below SLO) | Next business day |

## Declaring A Quality Incident

Quality incidents require a different trigger mechanism than technical incidents because they do not fire alerts automatically:

**Trigger conditions for a quality incident declaration:**
1. Eval score drops below P3 threshold for two consecutive daily eval runs
2. Negative user feedback rate exceeds 2× the 30-day average
3. Manual review of sample responses shows systematic quality failure
4. Canary prompt similarity drop detected by automated monitoring

**Declare by:**
1. Opening an incident ticket with severity classification
2. Identifying the likely scope: which models, prompts, or features are affected
3. Assigning a primary responder and a backup

## Incident Response Runbook Structure

Every AI platform incident type should have a runbook. The structure:

```markdown
# Runbook: [Incident Type]

## Symptoms
What operators and users observe.

## Immediate Actions (first 5 minutes)
What to do before diagnosis.

## Diagnosis Tree
Step-by-step investigation procedure with decision branches.

## Mitigation Options
Ordered list: fastest recovery first.

## Verification
How to confirm the incident is resolved.

## Escalation
When to escalate and to whom.

## Post-Mortem Trigger
Criteria that require a post-mortem.
```

## Sample Runbook: Provider Timeout Incident

```markdown
# Runbook: Model Provider Timeout

## Symptoms
- TTFT p95 > 5 seconds for 5+ minutes
- gateway_fallback_events_total increasing
- Users reporting "slow" or "stuck" responses

## Immediate Actions
1. Check provider status page
2. Check gateway fallback events — is fallback activating correctly?
3. If fallback is not activating: verify circuit breaker configuration

## Diagnosis Tree
- If provider status page shows outage: activate manual fallback, wait
- If provider status page shows healthy: check network path gateway→provider
- If network is healthy: check if a specific model endpoint is slow (not all)
- If one endpoint slow: switch traffic to alternative model in gateway config

## Mitigation
1. (fastest) Enable fallback at gateway if not automatic
2. Switch to alternative model endpoint in gateway routing config
3. If no alternative available: activate degraded mode (respond without model)

## Verification
- TTFT p95 returns to baseline (< 1 second)
- Fallback event counter stops growing

## Escalation
If provider outage > 1 hour and no fallback available: escalate to platform lead
```

## Sample Runbook: Quality Degradation Incident

```markdown
# Runbook: Quality Degradation

## Symptoms
- Eval score below P3 threshold on consecutive runs
- Negative feedback rate spike
- User reports: "answers feel different/worse"

## Immediate Actions
1. Identify when the degradation started (eval score trend)
2. Check for recent deployments: prompt change, model update, config change

## Diagnosis Tree
- Recent prompt version change? → compare current vs previous eval scores
- Recent model version update? → run eval against previous model pin
- No recent changes? → check for silent provider model update (canary prompts)
- No changes, no provider update? → check RAG index freshness

## Mitigation
1. (fastest) Roll back prompt to last good version
2. Repin model to previous version
3. Force re-ingest RAG index if staleness is the cause
4. If no known cause: add extra eval sampling, escalate for investigation

## Verification
- Eval score returns above SLO threshold on next run
- No continued negative feedback spike

## Post-Mortem Trigger
Quality below SLO for > 48 hours OR eval score below 0.65
```

## Post-Mortem Guidelines For AI Incidents

AI post-mortems should include AI-specific sections alongside standard SRE post-mortem structure:

- **Quality impact assessment**: what fraction of responses during the incident were degraded?
- **Detection gap**: was there an observability gap that delayed detection?
- **Prompt/model review**: what changed and should evaluation gates have caught it?
- **Eval dataset update**: does the incident reveal a gap in the evaluation dataset?
- **Runbook update**: does the runbook need new diagnostic steps based on what was learned?

The last two items are how reliability investments compound: each incident improves the evaluation dataset and the runbook, making the platform more resilient to the same type of failure in the future.
