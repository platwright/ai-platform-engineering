# Chapter 02 - Token Cost Modeling for Hosted APIs

## The Cost Formula

All major hosted API providers bill per million tokens (M tokens), with separate rates for input and output:

```
cost_per_request = 
    (prompt_tokens / 1_000_000) × input_price_per_M
  + (completion_tokens / 1_000_000) × output_price_per_M
```

## Reference Pricing (Mid-2025)

These are representative prices for planning. Check current provider pages before any financial decision.

| Model | Input $/M | Output $/M | Notes |
|---|---|---|---|
| GPT-4o mini | $0.15 | $0.60 | Best cost for most tasks |
| GPT-4o | $5.00 | $15.00 | Frontier capability |
| Claude 3 Haiku | $0.25 | $1.25 | Fast, cheap |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Strong reasoning |
| Gemini 1.5 Flash | $0.075 | $0.30 | Very cheap for volume |
| Gemini 1.5 Pro | $3.50 | $10.50 | |
| Llama 3.1 70B (via Together) | $0.88 | $0.88 | Open-weight, hosted |

Output tokens are consistently more expensive than input tokens (typically 3–5×). Systems with long outputs cost disproportionately more.

## Workload Cost Estimation

For a RAG chat workload:

```python
# Example: RAG chat with moderate context
system_prompt:      600 tokens
retrieved_context: 1,800 tokens  # 5 chunks × ~360 tokens each
user_message:        100 tokens
─────────────────────────────────
total_input:       2,500 tokens

typical_output:      300 tokens  # conversational response

# At GPT-4o mini pricing:
cost_per_request = (2500 / 1e6 * 0.15) + (300 / 1e6 * 0.60)
                 = $0.000375 + $0.000180
                 = $0.000555 per request

# At 1,000 requests/day:
daily_cost = 1000 * 0.000555 = $0.555/day
monthly_cost = 0.555 * 30 = $16.65/month
```

## Volume Projections

Scale the per-request estimate to production volume:

```python
def project_monthly_cost(
    requests_per_day: int,
    avg_input_tokens: int,
    avg_output_tokens: int,
    input_price_per_m: float,
    output_price_per_m: float
) -> float:
    cost_per_request = (avg_input_tokens / 1e6 * input_price_per_m +
                        avg_output_tokens / 1e6 * output_price_per_m)
    return cost_per_request * requests_per_day * 30

# Sample projection
print(project_monthly_cost(
    requests_per_day=10_000,
    avg_input_tokens=2_500,
    avg_output_tokens=300,
    input_price_per_m=0.15,
    output_price_per_m=0.60
))
# → $166.50/month
```

## Output-Heavy Workloads Are Expensive

Workloads with long outputs (summarization, document generation, code synthesis) have a dramatically different cost profile:

```
RAG chat (300 output tokens):     $0.000555 / request
Long-form summary (2,000 output): $0.001575 / request  → 2.8× more expensive
Code generation (5,000 output):   $0.003375 / request  → 6× more expensive
```

Set appropriate `max_tokens` limits for each use case and ensure they reflect the actual content requirements.

## Break-Even vs Self-Hosting

A rough break-even calculation:

```python
def monthly_hosted_cost(tokens_per_month: int, blended_rate: float) -> float:
    return (tokens_per_month / 1e6) * blended_rate

def monthly_self_hosted_cost(gpu_hours: float, hourly_rate: float) -> float:
    return gpu_hours * hourly_rate  # 720 hours per month × GPU rate

# Example: 500M tokens/month at $3/M blended rate
hosted = monthly_hosted_cost(500_000_000, 3.0)  # $1,500/month

# One A10G at $1.50/hour (reserved): 720 × 1.50 = $1,080/month
# But GPU serves ~200M tokens/month at reasonable utilization
# For 500M tokens: need 2-3 GPUs → $2,160–$3,240/month
# Also: engineering ops cost, not included

# At this volume: hosted is cheaper
# At 5B tokens/month: self-hosted becomes competitive
```

The calculation changes significantly with:
- model selection (open-weight vs frontier)
- reserved vs on-demand GPU pricing
- GPU utilization rate
- engineering ops cost

## Provider Discounts

Most providers offer volume discounts, commitment discounts, or batch processing APIs at reduced rates:

- **Batch API** (OpenAI, Anthropic): 50% discount for requests that can wait 24 hours — useful for evaluation runs, batch summarization, nightly processing jobs
- **Committed use**: annual commitments may reduce rates by 20–40%
- **Enterprise agreements**: available at high volume, terms vary

For evaluation jobs (Module 11), always use batch APIs when available to reduce eval cost by 50%.
