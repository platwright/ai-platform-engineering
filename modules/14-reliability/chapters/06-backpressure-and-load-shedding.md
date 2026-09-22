# Chapter 06 - Backpressure and Load Shedding

## Why Serving Has Bounded Capacity

A model server has a fixed amount of GPU memory. That memory is consumed by model weights, activations, and KV cache. When too many concurrent requests are served, the KV cache fills up, generation slows dramatically, and the queue grows. In extreme cases, the GPU OOMs and the serving process crashes.

Unlike a web server that can scale horizontally to absorb any traffic spike, model serving requires expensive GPU hardware. Capacity has real boundaries. When traffic exceeds those boundaries, the serving layer must protect itself rather than accepting all traffic and degrading for everyone.

## Queue Depth As The Key Signal

The most useful signal for AI serving backpressure is queue depth: how many requests are waiting to be processed.

```
queue_depth = 0–5:    healthy, low load
queue_depth = 5–20:   moderate load, latency beginning to grow
queue_depth = 20–50:  high load, latency significantly elevated
queue_depth = 50+:    overloaded, reject new requests
```

Queue depth is actionable. If it is growing, either add serving capacity (more replicas) or reduce incoming traffic (rate limiting, load shedding).

## Backpressure Strategies

### Gateway-Level Queue Limits

The gateway limits how many requests it accepts before rejecting with 429:

```python
from collections import deque
import threading

class RequestQueue:
    def __init__(self, max_size: int = 50):
        self._queue = deque()
        self._lock = threading.Lock()
        self.max_size = max_size

    def enqueue(self, request: dict) -> bool:
        with self._lock:
            if len(self._queue) >= self.max_size:
                log_metric("queue_full_rejections_total")
                return False
            self._queue.append(request)
            return True
```

A 429 response returned immediately is better than a 30-second wait followed by a timeout. The client knows to back off; an indefinitely queued client does not.

### Per-Tenant Concurrency Limits

Prevent one tenant from consuming all serving capacity:

```python
TENANT_MAX_CONCURRENT = 10

tenant_in_flight: dict[str, int] = {}

def check_tenant_concurrency(tenant: str) -> bool:
    current = tenant_in_flight.get(tenant, 0)
    if current >= TENANT_MAX_CONCURRENT:
        log_metric("tenant_concurrency_limit_hit", {"tenant": tenant})
        return False  # reject
    tenant_in_flight[tenant] = current + 1
    return True
```

## Load Shedding

Load shedding is the deliberate rejection of low-priority requests during overload conditions to protect high-priority traffic.

### Priority-Based Shedding

Define request priorities based on business rules:

```python
PRIORITY = {
    "interactive_user_chat": 1,   # highest priority
    "agent_query":           2,
    "rag_query":             3,
    "batch_evaluation":      4,   # lowest priority, first to shed
    "background_reindex":    5,
}

def should_shed(request: dict, queue_depth: int) -> bool:
    priority = PRIORITY.get(request["type"], 3)
    # Shed low-priority requests when queue is high
    shed_threshold = queue_depth / 10  # 0.0 at depth 0, 1.0 at depth 100
    return priority > 3 and random.random() < shed_threshold
```

Background batch jobs are shed first. Interactive user requests are the last to be shed.

### Adaptive Load Shedding

Automatically adjust the shedding rate based on current system load:

```python
def compute_shed_probability(queue_depth: int, max_queue: int) -> float:
    if queue_depth < max_queue * 0.5:
        return 0.0      # no shedding below 50% of max
    elif queue_depth < max_queue * 0.8:
        # Linear increase from 0% to 50% shedding
        return (queue_depth - max_queue * 0.5) / (max_queue * 0.3)
    else:
        return 0.8      # cap at 80% shedding even at full queue
```

Never shed 100% of traffic — that is a complete outage, not load management.

## What To Return On Load Shed

A useful HTTP 429 response includes:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 5
Content-Type: application/json

{
  "error": "rate_limited",
  "message": "Service is currently at capacity. Please retry after 5 seconds.",
  "retry_after_seconds": 5
}
```

The `Retry-After` header tells compliant clients how long to wait before retrying. Clients that respect this header spread their retries over time, reducing the thundering herd.

## vLLM Backpressure Integration

vLLM's API server returns 429 when the scheduler queue is full. Configure the maximum queue size:

```bash
vllm serve model-name --max-num-seqs 256  # max concurrent sequences
```

When `max-num-seqs` is reached, vLLM returns a 429 with appropriate messaging. The gateway should propagate this 429 to the client rather than retrying on its own.

## Monitoring Backpressure

Track these signals as backpressure health indicators:

```promql
# Queue depth trend
vllm_num_requests_waiting

# Load shedding rate
rate(request_shed_total[5m])

# Per-tenant concurrency limit hits
rate(tenant_concurrency_limit_hit_total[5m])

# 429 rate seen by clients
rate(http_requests_total{status="429"}[5m])
```

A rising 429 rate to clients may be acceptable (backpressure working as designed) or may indicate the platform needs capacity increase (sustained high demand).
