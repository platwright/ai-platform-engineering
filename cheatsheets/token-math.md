# Token Math Cheatsheet

## Rough Conversion Rules

| Unit | Token Approximation |
|---|---|
| 1 English word | ~1.3 tokens |
| 1 character | ~0.25 tokens |
| 1 sentence (~15 words) | ~20 tokens |
| 1 paragraph (~100 words) | ~130 tokens |
| 1 page (~400 words) | ~500 tokens |
| 1,000 words | ~1,300 tokens |

These approximations work for English prose. Code, non-Latin scripts, numbers, and special characters tokenize differently.

## Context Window Budget Template

```
system_prompt:         _____ tokens
retrieved_context:     _____ tokens
conversation_history:  _____ tokens
current_user_turn:     _____ tokens
output_reserve:        _____ tokens
─────────────────────────────────────
Total:                 _____ tokens
Model max:             _____ tokens
Headroom:              _____ tokens
```

## Cost Estimation Formula

### Hosted API (per request)

```
cost = (input_tokens / 1_000_000 × input_price)
     + (output_tokens / 1_000_000 × output_price)
```

### Hosted API (monthly)

```
monthly_cost = daily_requests × avg_total_tokens / 1_000_000 × blended_rate × 30
```

### Example At Current (mid-2025) Pricing

| Model | Input $/M | Output $/M |
|---|---|---|
| GPT-4o mini | $0.15 | $0.60 |
| GPT-4o | $5.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Gemini 1.5 Flash | $0.075 | $0.30 |

Prices change frequently. Always check the current provider pricing page.

### 1M Tokens/Day Cost Examples

At 1M input tokens/day + 200K output tokens/day:

| Model tier | Estimated monthly cost |
|---|---|
| Cheap small model | ~$10–50/month |
| Mid-tier model | ~$300–600/month |
| Frontier model | ~$4,000–8,000/month |

## Context Length Impact On GPU Memory

KV cache memory per request (approximate):

```
kv_cache_bytes ≈ 2 × num_layers × num_heads × head_dim × seq_len × bytes_per_element
```

Practical rough guide for a 7B model (FP16):

| Context length | Approx KV cache per request |
|---|---|
| 2,048 tokens | ~0.5 GB |
| 8,192 tokens | ~2 GB |
| 32,768 tokens | ~8 GB |
| 128,000 tokens | ~30 GB |

Longer contexts dramatically reduce the number of concurrent requests a GPU can serve.

## Checking Token Usage In A Response

```bash
# With curl against an OpenAI-compatible endpoint
curl ... | jq '.usage'

# Expected output
{
  "prompt_tokens": 843,
  "completion_tokens": 142,
  "total_tokens": 985
}
```

## tiktoken Quick Reference (OpenAI Models)

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
tokens = enc.encode("Your text here")
print(f"Token count: {len(tokens)}")
```

Install: `pip install tiktoken`

## Hugging Face Tokenizer Quick Reference (Open-Weight Models)

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
tokens = tokenizer.encode("Your text here")
print(f"Token count: {len(tokens)}")
```

Install: `pip install transformers`
