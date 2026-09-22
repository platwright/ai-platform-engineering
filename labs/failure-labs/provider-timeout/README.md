# Failure Lab: Provider Timeout

**Covers**: Module 08 (AI Gateway), Module 14 (Reliability)

**Difficulty**: Intermediate

**Estimated time**: 45–60 minutes

---

## Objective

Configure the AI gateway to call a provider that always times out. Observe how each layer of the stack handles the failure and implement a fallback recovery path.

---

## Prerequisites

- Project 01 running locally
- The AI gateway service from `platform/docker/ai-gateway-stack.compose.yml` available
- Basic familiarity with Module 08 and Module 14 material

---

## Step 1: Setup — Create The Slow Provider

Add a new provider entry to `projects/project-01-model-api/config/app.json` that always sleeps before responding:

```json
{
  "alias": "acme-always-timeout",
  "type": "mock",
  "fixture_path": "fixtures/chat-success.json",
  "latency_ms": 35000,
  "weight": 1.0
}
```

A `latency_ms` of 35,000 ms (35 seconds) will exceed any reasonable timeout configuration.

---

## Step 2: Create The Failure Condition

Update the AI gateway configuration (`platform/docker/ai-gateway-service/config/app.json`) to route all requests to `acme-always-timeout`:

```json
"routing": {
  "default_provider": "acme-always-timeout",
  "fallback_provider": "acme-always-timeout"
}
```

This disables the fallback — both primary and fallback point to the broken provider.

---

## Step 3: Observe The Symptoms

Start Project 01 in a terminal:

```bash
python projects/project-01-model-api/app.py serve
```

In another terminal, send a request through the gateway:

```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test timeout behavior"}'
```

Observe:
- How long does the request hang before returning?
- What HTTP status code does the gateway return?
- What does the error body say?
- Is a run artifact written? What does it contain?

Record your observations in `my-notes/failure-lab-timeout.md`.

---

## Step 4: Diagnose

Check the Project 01 server logs. What do they show?

```bash
# Look for timeout events in the gateway logs
docker compose -f platform/docker/ai-gateway-stack.compose.yml logs ai-gateway
```

Questions to answer:
1. At which layer did the timeout occur — application, gateway, or provider?
2. Did the timeout propagate cleanly or did it cause an unexpected error shape?
3. Was the failure silent or was it logged?

---

## Step 5: Implement Recovery — Restore Fallback

Update the gateway configuration to restore a working fallback provider:

```json
"routing": {
  "default_provider": "acme-always-timeout",
  "fallback_provider": "acme-reliable"
}
```

Resend the request. Observe:
- Does the fallback activate automatically?
- What does the gateway log show for the fallback event?
- Does the response indicate a fallback was used?
- Is latency higher due to the timeout + retry cycle?

---

## Step 6: Recovery — Reduce Timeout

As an alternative recovery strategy, reduce the provider timeout so failures are detected faster:

In the gateway config, set `timeout_seconds` to `3` for the default provider.

Resend the same request and compare:
- How does the perceived latency change?
- At what timeout value does user experience become acceptable?

---

## Step 7: Prevention

In `my-notes/failure-lab-timeout.md`, describe:

1. What monitoring signal would have detected this failure before users reported it?
2. What alert condition would you write for this scenario in Prometheus alertmanager?
3. What is the minimum set of changes that would make this stack resilient to a single provider timeout?
4. What happens if both the primary and fallback providers time out simultaneously? How would you handle that?

---

## Expected Outcomes

| Observation | Expected |
|---|---|
| Request hangs with no fallback | Yes — full timeout duration |
| Gateway returns 503 or 504 | Yes |
| Fallback activates when configured | Yes — reduced total latency |
| Run artifact captures the failure | Yes — `success: false`, error details present |

---

## Cleanup

Restore the gateway configuration to working defaults:

```bash
# Reset to the original example config
cp platform/docker/ai-gateway-service/config/app.example.json \
   platform/docker/ai-gateway-service/config/app.json
```

Remove `acme-always-timeout` from the Project 01 provider list.
