# Chapter 07 - AI-Aware Load Testing

## What Standard Load Tests Miss

A standard HTTP load test (wrk, k6, Locust with simple POST requests) sends requests at a target rate and measures HTTP response time. This tells you:
- whether the server crashes under load
- approximate request rate the server can sustain
- HTTP-level latency

It does not tell you:
- whether TTFT is acceptable for interactive users (streaming responses appear fast even if total generation is slow)
- whether the quality of responses degrades under load
- how token generation rate changes with concurrency
- whether the model queue grows unboundedly or stabilizes

## The AI Load Test Dimensions

A complete AI load test measures:

| Dimension | Metric | Why It Matters |
|---|---|---|
| Availability | Error rate by status code | Basic correctness under load |
| First-byte latency | TTFT p50, p95, p99 | User experience |
| Generation speed | Tokens per second | User reading experience |
| Total latency | End-to-end p50, p95, p99 | SLO compliance |
| Queue behavior | Queue depth over time | Serving capacity signal |
| Cost | Total tokens generated | Budget impact of load |
| Quality (optional) | Score on sample eval cases | Whether quality degrades under load |

## Realistic Prompt Distribution

The most important factor for a meaningful load test is using a realistic prompt distribution. Sending 5-token prompts to test a system that handles 800-token prompts in production produces useless results.

Characterize your production prompt distribution:
```python
import statistics

# Collect from production logs (anonymized)
prompt_lengths = [843, 1205, 672, 988, 1450, ...]

print(f"p50: {statistics.median(prompt_lengths)} tokens")
print(f"p95: {sorted(prompt_lengths)[int(len(prompt_lengths)*0.95)]} tokens")
print(f"p99: {sorted(prompt_lengths)[int(len(prompt_lengths)*0.99)]} tokens")
```

Use the Project 02 benchmark's prompt set as a starting point, but supplement it with prompts that reflect your actual use case.

## Using Project 02 For Load Testing

```bash
# Low concurrency baseline
python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode http \
  --endpoint http://localhost:8001/v1/chat/completions \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --concurrent 1 \
  --requests 20

# Medium concurrency
python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --concurrent 5 --requests 50

# High concurrency
python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --concurrent 20 --requests 100
```

Compare the metrics across concurrency levels to find the point where TTFT degrades non-linearly.

## Load Test Ramp Pattern

A ramp test is more revealing than a single fixed concurrency test:

```
Concurrency: 1 → 5 → 10 → 20 → 30 → 40 → 50
Duration at each level: 60 seconds
Measurement: TTFT p95, tokens/sec, queue depth, error rate at each level
```

The inflection point — where TTFT starts growing faster than concurrency — is your serving capacity boundary.

## Analyzing Results

A well-analyzed load test produces a capacity table:

| Concurrency | TTFT p50 | TTFT p95 | Tok/s | Queue Depth | Error Rate |
|---|---|---|---|---|---|
| 1 | 280ms | 380ms | 45 | 0 | 0% |
| 5 | 290ms | 410ms | 43 | 0 | 0% |
| 10 | 320ms | 550ms | 40 | 2 | 0% |
| 20 | 480ms | 1200ms | 35 | 8 | 0% |
| 30 | 900ms | 2800ms | 28 | 18 | 0.5% |
| 40 | 1800ms | 5200ms | 22 | 35 | 3% |

From this table:
- TTFT SLO of 1000ms at p95 → max sustainable concurrency is ~25
- Error rate starts at concurrency 30 → queue fills at that point
- Scale-out trigger: add a replica before reaching concurrency 25

## Load Testing Without GPU Hardware

Without GPU hardware, load tests run against CPU-based serving (Ollama with a small model) or mock servers. Results will not match GPU serving performance, but load testing patterns and analysis approaches still apply.

Use the `--mode mock` flag in the Project 02 benchmark to practice the analysis workflow without real hardware.
