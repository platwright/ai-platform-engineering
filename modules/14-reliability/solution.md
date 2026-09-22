# Module 14 Solution

## Failure Taxonomy Classification Reference

1. CUDA OOM → **Infrastructure failure**
2. Stale RAG index returning wrong context with HTTP 200 → **Data failure** (quality dimension)
3. Prompt update causes shorter responses → **Configuration failure** (quality dimension)
4. OpenAI 500 errors → **Provider failure**
5. One tenant's batch job fills the queue → **Cascading failure** (started as a capacity issue, cascaded to affect all tenants)

## SLO Reference Design For Sample-Chat

```yaml
slos:
  - name: availability
    sli: "success_requests / total_requests"
    target: 0.995
    error_budget_minutes_per_month: 216  # 0.005 × 30 × 24 × 60

  - name: ttft_latency
    sli: "count(ttft < 800ms) / total_requests"
    target: 0.95
    window: 5m
    error_budget_fraction: 0.05

  - name: rag_quality
    sli: "daily_eval_pass_rate"
    target: 0.80
    error_budget: "20% of eval runs may be below threshold per 7-day window"
    measurement: "scheduled eval job, writes to ai_platform_eval_score metric"
```

## Provider Timeout Simulation Findings

The mock `acme-rate-limited` provider in Project 01 introduces a fixed delay. In the default configuration:

- There is no retry configured — the first failure is the final failure
- There is no fallback provider configured — the error propagates to the caller
- The timeout may not be set, causing indefinite wait

To implement basic retry-with-backoff, the provider adapter would need:

```python
# In the provider adapter
import random, time

def call_with_retry(self, messages, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return self._call(messages)
        except (TimeoutError, ProviderError) as e:
            if attempt == max_attempts - 1:
                raise
            delay = random.uniform(0, 1.0 * (2 ** attempt))
            time.sleep(delay)
```

## Missing Index Behavior Reference

When the index file is missing, Project 03 should:
- Return an error indicating the service is not available (preferred)
- Or return zero results with a clear indication that no context was retrieved

What it should NOT do:
- Silently proceed with empty context and return a model response that appears grounded
- Crash the entire application process

If the application proceeds silently with empty context, the model will generate from training knowledge and present it as if it were retrieved — a quality failure with no technical error signal.

## Sample Runbook: Provider Timeout

```markdown
# Runbook: Provider Timeout Incident

## Symptoms
- Users report slow or stuck responses
- Gateway logs show provider calls timing out
- TTFT p95 alert fires

## Immediate Actions (< 5 minutes)
1. Check provider status page
2. Confirm gateway is logging fallback events
3. If fallback is NOT activating: manually switch routing in gateway config

## Diagnosis Tree
Provider status page shows outage?
  → Yes: activate manual fallback, monitor
  → No: check network path, check specific model endpoint

Network healthy, provider healthy?
  → Yes: check if specific model is overloaded (try different model)
  → No: escalate to network team

## Mitigation
1. Manual fallback via gateway routing config change
2. If no fallback: enable degraded mode (return "service temporarily unavailable")

## Verification
- TTFT p95 returns to baseline
- No new timeout events in gateway logs

## Escalation
Provider outage > 1 hour with no fallback: escalate to platform lead
```
