# Chapter 02 - Scaling the Application Tier

## Application Tier Characteristics

The application tier (sample-chat, sample-rag, sample-agent) is typically the easiest layer to scale because it is stateless. Application pods do not hold conversation state, model weights, or large in-memory caches. They receive a request, call downstream services, and return a response.

This makes horizontal scaling straightforward: add replicas, distribute traffic through a load balancer.

## When The Application Tier Is The Bottleneck

The application tier is often NOT the bottleneck in AI systems. But it can be when:

- request processing is CPU-intensive (tokenization, response parsing, logging)
- the application holds per-request state that grows with conversation history
- a single-process Python application blocks on I/O without async handling
- session affinity routes all requests from a user to one replica, creating hotspots

## Horizontal Scaling

Standard Kubernetes horizontal pod autoscaling on CPU/memory works well for stateless application pods:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sample-chat-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sample-chat
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

CPU-based HPA is appropriate here because the application tier is genuinely CPU-bound (request parsing, JSON serialization) rather than GPU-bound.

## Connection Pooling

When the application tier scales to many replicas, each replica holds HTTP connections to downstream services. Without connection pooling, the number of connections to the model server grows as:

```
connections = app_replicas × threads_per_replica

10 replicas × 10 threads = 100 connections to the model server
```

At high replica counts, this exhausts the model server's connection limit. Use a connection pool per downstream service:

```python
from urllib3 import PoolManager

# One pool per downstream service, shared across all threads in a replica
MODEL_API_POOL = PoolManager(
    num_pools=1,
    maxsize=20,      # max connections per replica to the model server
    retries=False
)
```

## Session Affinity

For conversation applications that maintain chat history, session affinity routes requests from the same session to the same application replica. This avoids fetching history from a central store on every request.

Session affinity is appropriate when:
- conversation history is small enough to fit in memory comfortably
- sessions are short-lived (minutes, not days)
- the history is not needed after the session ends

Session affinity is a problem when:
- a replica fails and all its sessions are lost (no redundancy for state)
- sessions are long-lived and pin load to specific replicas
- application pods restart frequently

The production alternative is to store conversation history externally (Redis, PostgreSQL) and abandon session affinity entirely. The application becomes truly stateless at the cost of one extra external call per request.

## Async vs Sync Request Handling

A synchronous single-threaded Python application can only handle one request at a time per replica. For AI applications that spend most of their time waiting for upstream calls, async I/O provides significantly better utilization:

```python
import asyncio
import aiohttp

async def handle_chat(request: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        # These calls happen concurrently, not sequentially
        rag_task = asyncio.create_task(query_rag(session, request["question"]))
        gateway_task = asyncio.create_task(call_gateway(session, request))
        
        context = await rag_task
        response = await gateway_task
        return {"response": response, "context": context}
```

Async handling allows a single replica to handle many concurrent in-flight requests while waiting for I/O, reducing the number of replicas needed for a given throughput target.
