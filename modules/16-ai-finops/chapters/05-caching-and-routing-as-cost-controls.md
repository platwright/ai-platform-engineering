# Chapter 05 - Caching and Routing as Cost Controls

## Caching Reduces Token Spend

Every request that hits the cache does not call the model, so no tokens are billed for it. Caching is one of the highest-leverage cost optimization levers when hit rates are reasonable.

## Prompt Caching (Exact Match)

Prompt caching stores the full model response for an exact prompt match:

```python
import hashlib

def cached_model_call(prompt: str, config: dict, cache) -> dict:
    cache_key = hashlib.sha256((prompt + str(config)).encode()).hexdigest()
    
    cached = cache.get(cache_key)
    if cached:
        cache_hits_counter.inc()
        return cached
    
    response = call_model(prompt, config)
    cache.set(cache_key, response, ttl=3600)  # 1-hour TTL
    return response
```

**When prompt caching is effective**:
- FAQ-style applications where many users ask the same question
- system prompt prefix caching (providers like OpenAI and Anthropic support server-side KV cache for repeated prefixes)
- evaluation runs where the same eval cases are run repeatedly

**When it is not effective**:
- conversational applications where each message is unique
- RAG queries where retrieved context changes the full prompt
- applications where user messages are highly varied

## Provider-Side KV Cache for Prefixes

OpenAI (and some other providers) support prompt caching for the repeated prefix portion of a prompt — typically the system prompt and any static boilerplate. This is automatic and free for most providers; you need only ensure the static portion comes first in the prompt.

```python
# GOOD: system prompt (cacheable prefix) comes first
messages = [
    {"role": "system", "content": LONG_STATIC_SYSTEM_PROMPT},  # 600 tokens, cached
    {"role": "user", "content": user_message}  # 100 tokens, billed
]

# BAD: system prompt varies per request, no caching benefit
messages = [
    {"role": "system", "content": f"You are assisting {user_name} from {user_org}"},
    ...
]
```

For workloads with large, repeated system prompts, provider-side KV caching can reduce input token costs by 50–80%.

## Semantic Caching

Semantic caching returns cached responses for semantically similar (not identical) queries. It requires an embedding lookup on every request to find similar cached queries.

**Cost analysis for semantic caching**:

```python
# Overhead cost per request (embedding for cache lookup)
cache_overhead = embedding_tokens / 1e6 * embedding_price  # e.g., $0.00001

# Savings per cache hit (model tokens saved)
tokens_saved_per_hit = avg_prompt_tokens + avg_completion_tokens
savings_per_hit = tokens_saved_per_hit / 1e6 * model_price

# Break-even hit rate:
# cache_overhead = savings_per_hit × hit_rate
# hit_rate = cache_overhead / savings_per_hit
break_even_hit_rate = cache_overhead / savings_per_hit
```

Semantic caching is only cost-positive above the break-even hit rate. For many workloads with varied user queries, this rate is 10–20% — not always achievable.

## Model Routing as a Cost Control

The AI gateway can route requests to different model tiers based on task characteristics:

```python
def select_model(request: dict, context: dict) -> str:
    # Cheap model for simple, short exchanges
    if context.get("message_length", 0) < 100 and not context.get("is_complex"):
        return "gpt-4o-mini"
    
    # Cheap model for classification tasks
    if request.get("task_type") == "classification":
        return "gpt-4o-mini"
    
    # More capable model for complex reasoning
    if context.get("requires_reasoning"):
        return "gpt-4o"
    
    # Default to cheap tier
    return "gpt-4o-mini"
```

**Tiered routing cost impact**:

If 80% of requests route to a cheap model ($0.60/M output) and 20% to a frontier model ($15.00/M output):

```
Blended output rate = 0.80 × 0.60 + 0.20 × 15.00 = $3.48/M
vs all-frontier:  $15.00/M → 78% cost reduction
vs all-cheap:     $0.60/M  → but some quality loss
```

Tiered routing provides most of the cost reduction of using only the cheap model while maintaining quality for requests that need it.

## Routing Decision Quality Gate

Every routing change must be evaluated:

1. Define the routing rule
2. Run the eval suite with the new routing applied to each case
3. Confirm quality SLO is maintained
4. Deploy and monitor real traffic quality signals

Never deploy a cost-reduction routing change without an eval run.
