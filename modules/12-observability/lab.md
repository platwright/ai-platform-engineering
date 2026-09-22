# Module 12 Lab

## Goal

Instrument the sample-rag request path to capture token usage and latency metrics, review the existing gateway request logs for operational signals, and design a minimal alert configuration.

## Prerequisites

- Project 03 (RAG platform) running with at least one ingested service
- Python 3.11+
- Basic familiarity with Prometheus metric types (Counter, Gauge, Histogram)

## Step 1 - Identify What The AI Gateway Already Logs

Start the AI gateway locally:

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml up --build
```

Send a test request:

```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain retrieval freshness.", "provider": "acme-fast"}'
```

Look at the gateway container logs:

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml logs ai-gateway
```

Identify which of these signals are already present in the logs:
- [ ] `prompt_tokens`
- [ ] `completion_tokens`
- [ ] request latency (ms)
- [ ] the selected model or provider
- [ ] any error information

Write down which signals are missing.

## Step 2 - Add Token Usage Logging To The Application

Open `applications/sample-rag/app.py`. Find the function that handles a query and returns a response. Add structured logging that captures the response metadata:

```python
import json, time, datetime

def log_request(question: str, response: dict, latency_ms: float):
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "question_length_chars": len(question),
        "prompt_tokens": response.get("usage", {}).get("prompt_tokens", 0),
        "completion_tokens": response.get("usage", {}).get("completion_tokens", 0),
        "total_tokens": response.get("usage", {}).get("total_tokens", 0),
        "latency_ms": round(latency_ms, 2)
    }
    print(json.dumps(entry))
```

Verify the log entries appear when you run a query:

```bash
python applications/sample-rag/app.py query --tenant team-a --question "What is retrieval freshness?"
```

## Step 3 - Add Latency Timing

Wrap the model call with timing to measure TTFT and total latency separately.

Hint: the sample-rag app uses `urllib.request` or a similar simple HTTP client. Capture the time before the request starts and the time after the first response chunk arrives (for TTFT) versus when the full response is received.

Document the latency you observe for a typical query:

```
Query: "What is retrieval freshness?"
Embed query:     ___ms
Vector search:   ___ms
Total retrieval: ___ms
LLM generation:  ___ms
Total:           ___ms
```

## Step 4 - Design A Prometheus Metrics Schema

Without implementing a full Prometheus exporter (that would require `prometheus_client`), design the metrics schema you would add to the RAG application:

Write a YAML file at `eval/observability-design.yaml`:

```yaml
metrics:
  - name: rag_query_total
    type: counter
    labels: [tenant, status]
    description: "Total RAG queries"

  - name: rag_query_duration_seconds
    type: histogram
    labels: [tenant]
    buckets: [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    description: "RAG query end-to-end duration"

  - name: rag_llm_prompt_tokens_total
    type: counter
    labels: [tenant, model]
    description: "Cumulative prompt tokens sent to the LLM"

  # Add at least 3 more metrics from the chapter material
```

## Step 5 - Design An Alert

Write a Prometheus alerting rule for one of the conditions from the chapter:

Options:
- TTFT p95 above threshold
- RAG zero-result query rate above threshold
- Token cost rate above threshold

Save it as `eval/sample-alert.yaml` in Prometheus YAML format.

## Step 6 - Reflection

In your workbook (`my-notes/module-12.md`), answer:

1. Which metric from the chapter would be most valuable to add to the sample-rag application first and why?
2. What information is currently missing from the gateway logs that would help diagnose a production incident?
3. Design the top row of a platform dashboard for Acme AI. What 5 panels would you put there?
4. Describe a scenario where the platform shows green HTTP metrics but is experiencing a real problem. How would you detect it?
