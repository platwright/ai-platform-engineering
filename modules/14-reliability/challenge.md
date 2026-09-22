# Module 14 Challenge

## Challenge 1 - Complete SLO Framework

Design a complete SLO framework for the Acme AI platform covering all four services (gateway, model serving, RAG platform, agent platform).

For each service, define:
- Two technical SLOs (availability and latency)
- One quality SLO
- Error budget calculation for each
- The error budget policy (what happens at 50%, 25%, 10%, 0%)

Present as a structured document in `my-solutions/module-14-slo-framework.md`.

## Challenge 2 - Retry and Fallback Implementation

Implement a `ReliableModelClient` class that wraps the Project 01 model API with:

1. **Retry with exponential backoff and jitter**: max 3 attempts, retriable errors only
2. **Fallback chain**: primary provider → secondary provider → degraded static response
3. **Circuit breaker per provider**: open after 5 consecutive failures, reset after 60 seconds
4. **Timeout per provider**: configurable connect and read timeouts

The class should expose a single `chat(messages)` method that handles all the above transparently.

Write unit tests that verify:
- retry happens on transient 500
- no retry on 400 or content filter
- fallback activates when all retries on primary fail
- circuit breaker opens after failure threshold
- circuit breaker resets after cooldown

## Challenge 3 - Load Shedding Middleware

Implement a simple load shedding middleware for the sample-chat application that:

1. Tracks a sliding window of in-flight requests
2. Rejects new requests with 429 when in-flight count exceeds a configurable threshold
3. Returns a `Retry-After` header with a calculated backoff value
4. Logs a metric each time a request is shed
5. Distinguishes between interactive requests (never shed) and batch requests (shed first)

Test it by sending concurrent requests beyond the threshold and confirming the rejection behavior.

## Challenge 4 - Quality Incident Drill

Simulate a quality incident and practice the response procedure:

1. Degrade the RAG system (rename the index file as in the lab)
2. Run the eval runner from Module 11 — confirm the score drops
3. Following your runbook, diagnose the cause
4. Apply the mitigation (restore the index)
5. Verify recovery by re-running the eval

Time yourself. Write in `my-notes/module-14-drill.md`:
- How long did detection take? (when did eval score alert fire?)
- How long did diagnosis take?
- How long did mitigation take?
- What would reduce each phase?

## Challenge 5 - Error Budget Dashboard

Design a Grafana dashboard row that shows error budget status for three SLOs:

For each SLO:
- Current value vs target (stat panel with threshold coloring)
- 7-day trend (time series)
- Budget remaining as a percentage (gauge)
- Days until budget exhausted at current burn rate (calculated)

Write the Prometheus queries for each panel. You do not need to implement in a real Grafana instance — structured PromQL queries with panel descriptions are sufficient.
