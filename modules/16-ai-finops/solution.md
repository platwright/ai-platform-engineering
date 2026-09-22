# Module 16 Solution

## Cost Calculation Reference

**Verification Check 1**:
- Input: 5,000 req/day × 1,500 tokens = 7.5M input tokens/day
- Output: 5,000 req/day × 400 tokens = 2M output tokens/day
- Daily input cost: 7.5 × $0.15 = $1.125
- Daily output cost: 2 × $0.60 = $1.20
- **Daily total: $2.325**
- **Monthly: ~$69.75**
- **Annual: ~$849**

A small team at modest volume. Easy to overlook until it scales.

## Routing Simulation Reference

At 1,000 requests/day × 30 days = 30,000 requests/month with 2,500 input and 300 output tokens:

```
All acme-fast:   30K × (2500×0.15 + 300×0.60) / 1e6 = $1.665/month
All acme-smart:  30K × (2500×3.00 + 300×15.00) / 1e6 = $360/month
80/20 blended:   24K fast + 6K smart = $1.332 + $72.00 = $73.33/month

Savings vs all-smart: (360 - 73.33) / 360 = 79.6%
```

Savings are not exactly 80% because output tokens are priced differently from input tokens and the ratio between them affects the blended calculation.

## Break-Even Analysis Reference

At 40% utilization, A10G ($1.50/hr):
- Effective rate: $1.50 / 0.40 = $3.75/effective hour
- At 40 tok/s, tokens per effective hour: 40 × 3600 × 0.40 = 57,600 tok/hr
- Cost per million tokens: $3.75 / (57,600/1,000,000) = $65/M
- GPT-4o mini output: $0.60/M → hosted is **dramatically cheaper** at 40% utilization

At 80% utilization:
- Effective rate: $1.50 / 0.80 = $1.875/effective hour
- Tokens per effective hour: 40 × 3600 × 0.80 = 115,200 tok/hr
- Cost per million tokens: $1.875 / (115,200/1,000,000) = $16.3/M
- Still more expensive than GPT-4o mini output ($0.60/M) for generation only

Self-hosting becomes competitive when the model is much larger (and the alternative is frontier model pricing at $15/M output) or when the volume is so high that even marginal cost improvements matter.

## Semantic Cache ROI Reference

For **Verification Check 6**:
- Embedding for cache lookup: 100 tokens × $0.0001/M = $0.00000001 per lookup (negligible)
- More relevant: embedding service API call = ~$0.0001 per lookup (depending on service)
- Cost saved per hit: $0.002 per request

At 5% hit rate:
- 100 lookups cost: 100 × $0.0001 = $0.01
- 5 hits save: 5 × $0.002 = $0.01
- Break-even: need > 5% hit rate to be cost-positive

The real overhead is complexity, not cost. Semantic caching adds an embedding service call, a vector similarity search, and a cache management system. This overhead is only justified if the hit rate is high enough to be meaningful (typically > 15-20% for it to be worth the engineering effort).

## Environment Controls Reference

Three dev-only cost controls (not appropriate for production):
1. **Automatic shutdown at 8 PM and restart at 8 AM weekdays**: avoids paying for overnight idle GPU
2. **Token quota per developer per month**: prevents accidental expensive experiments from running unchecked
3. **Default to cheapest model tier with no override convenience**: makes expensive model use a deliberate choice

Each of these would harm production: shutdowns disrupt users, quotas limit user requests, and default cheap models may miss production quality requirements.
