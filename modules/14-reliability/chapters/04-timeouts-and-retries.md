# Chapter 04 - Timeouts and Retries

## Why Timeouts Are Essential

A model API call without a timeout will wait indefinitely if the provider is slow or unresponsive. In a high-concurrency service, indefinitely-waiting requests consume connection pool slots and eventually exhaust resources, causing all new requests to fail even if the provider recovers.

Every outbound call in an AI platform must have an explicit timeout. This includes:
- model provider API calls
- embedding service calls
- vector database queries
- reranker calls
- tool executions from agents

## Timeout Layers

Set timeouts at multiple layers, each tighter than the one above:

```
User-facing SLO: respond within 8 seconds

Application timeout: 7 seconds (headroom before SLO breach)
Gateway timeout: 6 seconds (headroom before application gives up)
LLM provider timeout: 5 seconds (headroom before gateway gives up)
  └─ connect timeout: 2 seconds (fail fast if provider is unreachable)
  └─ read timeout: 5 seconds (fail if response stops mid-stream)
```

If the innermost timeout fires, each outer layer has time to handle it cleanly rather than also timing out.

## TTFT Timeout vs End-to-End Timeout

For streaming responses, there are two distinct timeout points:

1. **TTFT timeout**: how long to wait for the first token to arrive
2. **Generation timeout**: how long to wait for the full response (after first token)

```python
def stream_with_timeout(provider_url: str, payload: dict) -> Generator:
    TTFT_TIMEOUT_SEC = 3.0
    GENERATION_TIMEOUT_SEC = 30.0

    with requests.post(provider_url, json=payload, stream=True,
                       timeout=(2.0, TTFT_TIMEOUT_SEC)) as r:
        first_token = False
        start = time.time()
        for chunk in r.iter_content(chunk_size=None):
            if not first_token:
                first_token = True
                # TTFT measured here
            if time.time() - start > GENERATION_TIMEOUT_SEC:
                raise TimeoutError("Generation timeout exceeded")
            yield chunk
```

## Retry Strategies

### What To Retry

Retries are appropriate for transient errors where the same request has a reasonable chance of succeeding on a subsequent attempt:

| Error | Retriable? | Reasoning |
|---|---|---|
| 500 Internal Server Error | Yes (with limit) | May be transient server-side issue |
| 503 Service Unavailable | Yes | Provider temporarily overloaded |
| Connection timeout | Yes | Transient network issue |
| Read timeout | Yes (carefully) | May indicate slow model, not failure |
| 429 Too Many Requests | Yes, after `Retry-After` | Rate limit is time-bounded |
| 400 Bad Request | No | Input is invalid; same request will fail again |
| 401 Unauthorized | No | Auth issue; retrying wastes the budget |
| Content filter block | No | Input triggered a policy; not transient |

### Exponential Backoff With Jitter

Fixed-interval retries synchronize across multiple clients and can amplify load. Exponential backoff with jitter spreads retries over time:

```python
import random, time

def retry_with_backoff(call_fn, max_attempts: int = 3, base_delay: float = 1.0):
    for attempt in range(max_attempts):
        try:
            return call_fn()
        except RetriableError as e:
            if attempt == max_attempts - 1:
                raise
            # Full jitter: random in [0, base_delay * 2^attempt]
            delay = random.uniform(0, base_delay * (2 ** attempt))
            time.sleep(delay)
```

For rate limit (429) responses, read the `Retry-After` header if present:

```python
except RateLimitError as e:
    retry_after = float(e.response.headers.get("Retry-After", base_delay * (2 ** attempt)))
    time.sleep(retry_after)
```

### Retry Budgets

Unlimited retries turn a slow provider into a retry storm. Set a maximum attempt count and a maximum elapsed time:

```python
MAX_ATTEMPTS = 3
MAX_ELAPSED_SEC = 10.0  # total time including retries must stay within this

start = time.time()
for attempt in range(MAX_ATTEMPTS):
    if time.time() - start > MAX_ELAPSED_SEC:
        raise TimeoutError("Retry budget exhausted")
    # attempt call
```

## Idempotency

Retrying a model API call is safe because inference is stateless and idempotent: sending the same prompt twice produces (different but semantically equivalent) responses, without side effects.

Retrying a tool execution is not always safe. A tool that writes data may have partially executed before the error. Tools with side effects must be idempotent (produce the same outcome if called twice) or must not be retried automatically.

```python
def execute_with_retry(tool_name: str, args: dict, is_idempotent: bool):
    max_attempts = 3 if is_idempotent else 1
    return retry_with_backoff(lambda: execute_tool(tool_name, args), max_attempts)
```

## Timeout Propagation

When a downstream service times out, the caller must also fail quickly rather than waiting for the full upstream timeout:

```python
# If RAG query times out, fail the LLM call too
try:
    context = rag.query(question, timeout=2.0)
except TimeoutError:
    context = ""  # or use a degraded path
    log_metric("rag_timeout_fallback")

# Proceed with LLM call using available context
response = llm.call(question, context=context, timeout=5.0)
```

This prevents timeout cascades where one slow service causes all dependent services to also time out, exhausting connection pools at every layer.
