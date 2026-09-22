# Module 14 Concepts

## AI Reliability Extends Beyond Availability

Conventional reliability engineering asks: is the system up? AI reliability must also ask: is the system correct? A model server at 99.9% uptime that returns hallucinated answers 30% of the time is not reliable by any useful definition.

## Two Distinct Failure Dimensions

Every AI platform reliability design must cover both dimensions simultaneously:

- **Technical failures**: the system returns an error, times out, or crashes
- **Quality failures**: the system returns a successful response that is wrong, irrelevant, or harmful

HTTP health checks catch the first dimension. Evaluation pipelines catch the second. Both are needed.

## Non-Determinism Complicates SLOs

LLM outputs are stochastic. The same input can produce different outputs across requests. This means SLOs for AI systems cannot be purely deterministic thresholds. Quality SLOs require statistical measurement (mean score, pass rate) and statistical alerting (burn rate over time, not instantaneous threshold crossings).

## Error Budgets Apply To Quality As Well As Availability

The error budget concept — you have X% of time where the SLO can be violated before you must slow down change velocity — applies equally to quality SLOs. If your quality score is declining across multiple deployments, the error budget for quality is burning. That should slow deployments just as a burning availability error budget would.

## Retries Are Not Free

Retrying a failed model call is sensible for transient errors. Retrying during a provider outage amplifies load and can trigger additional rate limiting. Retry policies must distinguish between retriable errors (transient 500s) and non-retriable errors (rate limits, content filter blocks, permanent failures). Exponential backoff with jitter is the baseline for any retriable pattern.

## Fallback Is A Feature That Can Also Fail

A fallback to a smaller or different model provider is a resilience strategy. It is also a code path that must be tested, monitored, and itself made reliable. A fallback chain that silently stops working is worse than no fallback: it creates false confidence during incidents.

## Backpressure Protects The Serving Layer

Model serving has bounded capacity. When requests arrive faster than they can be served, queueing is the natural response. Unbounded queuing leads to user-visible latency explosion and eventual resource exhaustion. Explicit backpressure — rejecting excess requests early with a 429 rather than letting them queue indefinitely — is more reliable behavior.
