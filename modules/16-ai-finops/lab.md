# Module 16 Lab

## Goal

Build a cost report script that reads gateway request logs, calculates per-tenant costs, and produces a formatted monthly summary.

## Prerequisites

- Project 01 running (to generate some request logs)
- Python 3.11+

## Step 1 - Generate Some Request Logs

Send a few requests through different providers to create sample log data:

```bash
python projects/project-01-model-api/app.py chat \
  --provider acme-fast --message "Explain what retrieval freshness is."

python projects/project-01-model-api/app.py chat \
  --provider acme-smart --message "What is the difference between chunking and embedding?"

python projects/project-01-model-api/app.py chat \
  --provider acme-fast --message "How does a circuit breaker work in AI systems?"
```

Look at the generated run artifacts in `projects/project-01-model-api/runs/`. These contain token usage data.

## Step 2 - Build The Cost Report Script

Create `eval/cost_report.py`:

```python
#!/usr/bin/env python3
"""
Reads run artifacts from Project 01 and generates a cost summary.
Demonstrates per-model cost attribution.
"""
import json
import glob
import os
from collections import defaultdict

# Pricing table ($ per million tokens)
PRICING = {
    "acme-fast":    {"input": 0.15,  "output": 0.60},
    "acme-smart":   {"input": 3.00,  "output": 15.00},
    "acme-rate-limited": {"input": 0.15, "output": 0.60},
    "default":      {"input": 1.00,  "output": 3.00},
}

def compute_cost(provider: str, prompt_tokens: int, completion_tokens: int) -> float:
    rates = PRICING.get(provider, PRICING["default"])
    return (prompt_tokens / 1e6 * rates["input"] +
            completion_tokens / 1e6 * rates["output"])

def load_run_artifacts(runs_dir: str) -> list:
    artifacts = []
    for path in glob.glob(os.path.join(runs_dir, "*.json")):
        try:
            with open(path) as f:
                data = json.load(f)
            artifacts.append(data)
        except (json.JSONDecodeError, KeyError):
            pass
    return artifacts

def generate_report(runs_dir: str) -> dict:
    artifacts = load_run_artifacts(runs_dir)
    by_provider = defaultdict(lambda: {
        "requests": 0, "prompt_tokens": 0,
        "completion_tokens": 0, "cost_usd": 0.0
    })

    for artifact in artifacts:
        provider = artifact.get("provider", "unknown")
        usage = artifact.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        cost = compute_cost(provider, prompt_tokens, completion_tokens)

        by_provider[provider]["requests"] += 1
        by_provider[provider]["prompt_tokens"] += prompt_tokens
        by_provider[provider]["completion_tokens"] += completion_tokens
        by_provider[provider]["cost_usd"] += cost

    total_cost = sum(v["cost_usd"] for v in by_provider.values())

    return {
        "total_requests": len(artifacts),
        "total_cost_usd": round(total_cost, 6),
        "by_provider": dict(by_provider)
    }

if __name__ == "__main__":
    runs_dir = "projects/project-01-model-api/runs"
    report = generate_report(runs_dir)
    print(json.dumps(report, indent=2))
```

## Step 3 - Run The Cost Report

```bash
python eval/cost_report.py
```

Review the output:
- What is the total cost for the requests you generated?
- Which provider is most expensive per request?
- What does the token distribution look like (prompt vs completion)?

## Step 4 - Project Monthly Cost

Extend the script to project monthly costs:

```python
# Add to the report function
REQUESTS_PER_DAY_ESTIMATE = 1000  # your projected daily volume

for provider, stats in report["by_provider"].items():
    if stats["requests"] > 0:
        avg_cost = stats["cost_usd"] / stats["requests"]
        monthly = avg_cost * REQUESTS_PER_DAY_ESTIMATE * 30
        stats["projected_monthly_usd"] = round(monthly, 2)
```

## Step 5 - Simulate Tiered Routing Cost Impact

Calculate what the cost would be if you routed 80% of requests to `acme-fast` and 20% to `acme-smart`:

```python
def simulate_routing(total_requests: int,
                     fast_fraction: float,
                     avg_tokens_in: int,
                     avg_tokens_out: int) -> dict:
    fast_cost = compute_cost("acme-fast",
        avg_tokens_in * total_requests * fast_fraction,
        avg_tokens_out * total_requests * fast_fraction)
    smart_cost = compute_cost("acme-smart",
        avg_tokens_in * total_requests * (1 - fast_fraction),
        avg_tokens_out * total_requests * (1 - fast_fraction))
    return {
        "blended_cost": fast_cost + smart_cost,
        "all_fast_cost": compute_cost("acme-fast",
            avg_tokens_in * total_requests, avg_tokens_out * total_requests),
        "all_smart_cost": compute_cost("acme-smart",
            avg_tokens_in * total_requests, avg_tokens_out * total_requests)
    }

result = simulate_routing(
    total_requests=30_000,   # 1,000/day × 30 days
    fast_fraction=0.80,
    avg_tokens_in=2500,
    avg_tokens_out=300
)
print(f"Blended (80/20):   ${result['blended_cost']:.2f}")
print(f"All fast:          ${result['all_fast_cost']:.2f}")
print(f"All smart:         ${result['all_smart_cost']:.2f}")
print(f"Savings vs all smart: {(1 - result['blended_cost']/result['all_smart_cost'])*100:.1f}%")
```

## Step 6 - Reflection

In `my-notes/module-16.md`:

1. What was the most expensive component in your cost breakdown, even with mock/free providers?
2. At your projected monthly volume, what would be the real cost using actual GPT-4o mini pricing?
3. Design a chargeback model for Acme AI that you could actually implement with the tooling from this course.
4. What is the single cost optimization change that would have the largest impact on the Acme AI platform budget?
