# Chapter 05 - Fallback and Graceful Degradation

## Fallback vs Graceful Degradation

These are related but distinct strategies:

- **Fallback**: when the primary path fails, switch to an alternative path that provides the same (or similar) functionality
- **Graceful degradation**: when a dependency is unavailable, continue serving with reduced capability rather than failing entirely

A system can use both. The RAG query path may fall back to a different embedding provider. If that also fails, the system may degrade gracefully by answering without retrieved context.

## Fallback Chains

A fallback chain defines the ordered set of alternatives to try when each option fails:

```python
MODEL_FALLBACK_CHAIN = [
    {"provider": "openai",     "model": "gpt-4o-mini",       "timeout": 5.0},
    {"provider": "anthropic",  "model": "claude-3-haiku",    "timeout": 5.0},
    {"provider": "local",      "model": "llama-3.1-8b",      "timeout": 10.0},
]

def call_with_fallback(messages: list) -> dict:
    for config in MODEL_FALLBACK_CHAIN:
        try:
            return call_model(messages, **config)
        except (TimeoutError, ProviderError) as e:
            log_fallback_event(config["provider"], str(e))
            continue
    raise AllProvidersFailedError("All fallback options exhausted")
```

Each fallback tier should be logged as a distinct event — not just as a successful request — so that sustained fallback use is visible in the observability stack.

## When To Fall Back

Define explicit triggers for fallback activation rather than catching all exceptions:

| Trigger | Fallback Action |
|---|---|
| Provider timeout (> 5s) | Try next provider in chain |
| Provider 5xx | Try next provider with backoff |
| Content filter block | Do not retry; return controlled error to user |
| Rate limit (429) | Wait for `Retry-After`, then try next provider |
| Circuit breaker open | Skip provider entirely, go to next in chain |

## Circuit Breakers

A circuit breaker tracks error rate for a provider and temporarily stops sending requests when errors exceed a threshold:

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 60.0):
        self.failures = 0
        self.state = "closed"       # closed = healthy, open = failing
        self.last_failure_time = 0.0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout

    def call(self, fn):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half_open"
            else:
                raise CircuitOpenError("Circuit breaker open")

        try:
            result = fn()
            if self.state == "half_open":
                self.state = "closed"
                self.failures = 0
            return result
        except Exception as e:
            self.failures += 1
            self.last_failure_time = time.time()
            if self.failures >= self.failure_threshold:
                self.state = "open"
            raise
```

Circuit breakers prevent retry storms: when a provider is down, the breaker opens and subsequent requests fail immediately without creating load on the broken provider.

## Graceful Degradation Patterns

### RAG Degradation

When the RAG pipeline is unavailable, continue serving with the model's training knowledge:

```python
def answer_with_rag(question: str) -> dict:
    try:
        context = rag.query(question, timeout=2.0)
        grounded = True
    except (TimeoutError, ServiceUnavailable):
        context = ""
        grounded = False
        log_metric("rag_degraded_mode_requests_total")

    response = llm.call(question, context=context)
    return {
        "response": response,
        "grounded": grounded,
        "degraded": not grounded
    }
```

The response should indicate to the caller (and ultimately the user) that the answer may not be grounded. Do not silently degrade.

### Model Tier Degradation

When the primary (high-quality) model is unavailable, fall back to a smaller model with a quality warning:

```python
def call_with_tier_degradation(question: str) -> dict:
    for tier in [("premium", "gpt-4o"), ("standard", "gpt-4o-mini")]:
        try:
            response = call_model(tier[1], question)
            return {"response": response, "model_tier": tier[0]}
        except ProviderError:
            log_metric("model_tier_degradation", {"degraded_to": tier[0]})
    raise AllTiersFailedError()
```

### Static Fallback Responses

For critical paths where any degradation is unacceptable, a static fallback message is better than an error page:

```
"I'm currently unable to access the knowledge base. Please try again in a moment,
or contact the platform team if this persists."
```

This is a last resort, not a primary strategy. It provides a better user experience than an HTTP 500 while clearly communicating that the system is not fully functional.

## Testing Fallback Paths

Fallback paths that are not tested regularly stop working. Test them deliberately:

1. **Chaos testing**: periodically route a small percentage of requests through the fallback path even when the primary is healthy
2. **Scheduled drill**: monthly exercise where the team manually triggers each fallback scenario and verifies behavior
3. **Automated fallback smoke test**: CI test that activates each fallback tier and confirms a valid response is returned

A fallback path that fails silently during an actual incident is worse than no fallback.
