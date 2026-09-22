# Python AI Snippets

Quick-reference snippets for common AI platform engineering tasks in Python. All snippets use the standard library unless otherwise noted.

---

## Token Estimation

Rough token estimate without a tokenizer (±10–15% accuracy):

```python
def estimate_tokens(text: str) -> int:
    """Approximate token count: ~4 characters per token for English text."""
    return max(1, len(text) // 4)
```

Estimate cost before sending a request:

```python
def estimate_cost_usd(
    prompt: str,
    max_completion_tokens: int,
    input_price_per_million: float,
    output_price_per_million: float,
) -> tuple[float, float]:
    """Returns (min_cost, max_cost) assuming max_completion_tokens output."""
    prompt_tokens = estimate_tokens(prompt)
    min_cost = prompt_tokens / 1_000_000 * input_price_per_million
    max_cost = min_cost + max_completion_tokens / 1_000_000 * output_price_per_million
    return round(min_cost, 8), round(max_cost, 8)
```

---

## OpenAI-Compatible HTTP Call (Standard Library)

```python
import json
import time
from urllib import error, request

def chat(
    base_url: str,
    model: str,
    messages: list[dict],
    api_key: str = "",
    timeout: float = 30.0,
    **kwargs,
) -> dict:
    """POST /v1/chat/completions and return the parsed response body."""
    url = base_url.rstrip("/") + "/v1/chat/completions"
    payload = {"model": model, "messages": messages, **kwargs}
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = request.Request(
        url=url,
        method="POST",
        data=json.dumps(payload).encode(),
        headers=headers,
    )
    start = time.perf_counter()
    with request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read())
    body["_latency_ms"] = round((time.perf_counter() - start) * 1000, 2)
    return body


# Usage
response = chat(
    base_url="http://localhost:8000",
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
)
text = response["choices"][0]["message"]["content"]
usage = response.get("usage", {})
```

---

## Retry With Exponential Backoff

```python
import random
import time

def with_retry(fn, max_attempts: int = 3, base_delay: float = 1.0):
    """Call fn() up to max_attempts times with jittered exponential backoff."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as exc:
            if attempt == max_attempts - 1:
                raise
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1.0)
            time.sleep(delay)
```

---

## Structured Output Validation

```python
import json

def parse_json_response(text: str, required_keys: list[str]) -> dict:
    """
    Extract JSON from model output that may contain surrounding prose.
    Raises ValueError if the JSON is invalid or required keys are missing.
    """
    # Find the first complete JSON object in the response
    start = text.find("{")
    end = text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON object found in response: {text[:200]}")
    candidate = text[start:end]
    try:
        obj = json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc
    missing = [key for key in required_keys if key not in obj]
    if missing:
        raise ValueError(f"Missing required keys: {missing}")
    return obj
```

---

## Prompt Template Rendering

```python
import re

def render_prompt(template: str, variables: dict[str, str]) -> str:
    """
    Replace {{variable_name}} placeholders. Raises if any placeholder
    is unreferenced or missing from variables.
    """
    found = set(re.findall(r"\{\{(\w+)\}\}", template))
    missing = found - set(variables)
    if missing:
        raise ValueError(f"Missing template variables: {missing}")
    result = template
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", value)
    return result
```

---

## Run Artifact Writer

```python
import json
from datetime import datetime, timezone
from pathlib import Path

def write_artifact(data: dict, runs_dir: str | Path = "runs") -> Path:
    """Write a timestamped JSON run artifact. Returns the file path."""
    dest = Path(runs_dir)
    dest.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    path = dest / f"run-{ts}.json"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
```

---

## Keyword-Based Eval Scorer

```python
def score_response(response: str, expected_keywords: list[str]) -> float:
    """
    Return the fraction of expected keywords present in the response.
    Case-insensitive. Returns 0.0–1.0.
    """
    if not expected_keywords:
        return 1.0
    lower = response.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in lower)
    return round(hits / len(expected_keywords), 4)
```

---

## Simple In-Memory Rate Limiter

```python
import time
from collections import deque

class RateLimiter:
    """Token-bucket style rate limiter. Thread-unsafe (single-threaded use only)."""

    def __init__(self, max_per_minute: int) -> None:
        self._max = max_per_minute
        self._window = deque()

    def allow(self) -> bool:
        now = time.time()
        while self._window and now - self._window[0] > 60.0:
            self._window.popleft()
        if len(self._window) >= self._max:
            return False
        self._window.append(now)
        return True
```

---

## Chunking Text For RAG Ingestion

```python
def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping word-level chunks.
    chunk_size and overlap are in words.
    """
    words = text.split()
    if not words:
        return []
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = end - overlap
    return chunks
```

---

## Context Window Budget Calculator

```python
def context_budget(
    model_context_tokens: int,
    system_prompt_tokens: int,
    conversation_history_tokens: int,
    retrieved_context_tokens: int,
    reserved_completion_tokens: int,
) -> dict:
    """Report how much of the context window is used and what remains."""
    used = system_prompt_tokens + conversation_history_tokens + retrieved_context_tokens
    available_for_completion = model_context_tokens - used
    safe_for_completion = available_for_completion - reserved_completion_tokens
    return {
        "model_context_tokens": model_context_tokens,
        "used_tokens": used,
        "reserved_completion_tokens": reserved_completion_tokens,
        "available_for_completion": available_for_completion,
        "safe_to_generate": safe_for_completion > 0,
        "margin_tokens": max(0, safe_for_completion),
        "utilization_pct": round(used / model_context_tokens * 100, 1),
    }
```

---

## Load Test Helper (stdlib only)

```python
import concurrent.futures
import statistics
import time

def load_test(fn, concurrency: int, total_requests: int) -> dict:
    """
    Call fn() total_requests times with up to concurrency concurrent workers.
    fn must return a dict with a 'latency_ms' key.
    """
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = [pool.submit(fn) for _ in range(total_requests)]
        for future in concurrent.futures.as_completed(futures):
            try:
                results.append(future.result())
            except Exception as exc:
                results.append({"latency_ms": None, "error": str(exc)})

    latencies = [r["latency_ms"] for r in results if r.get("latency_ms") is not None]
    errors = [r for r in results if r.get("latency_ms") is None]
    sorted_lat = sorted(latencies)

    return {
        "total": total_requests,
        "success": len(latencies),
        "errors": len(errors),
        "p50_ms": statistics.median(sorted_lat) if sorted_lat else None,
        "p95_ms": sorted_lat[int(len(sorted_lat) * 0.95)] if sorted_lat else None,
        "p99_ms": sorted_lat[int(len(sorted_lat) * 0.99)] if sorted_lat else None,
        "min_ms": sorted_lat[0] if sorted_lat else None,
        "max_ms": sorted_lat[-1] if sorted_lat else None,
    }
```
