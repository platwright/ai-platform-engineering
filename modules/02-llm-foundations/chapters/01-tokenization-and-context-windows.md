# Chapter 01 - Tokenization and Context Windows

## What Tokenization Is

When you send text to a language model, the model does not see characters or words. It sees a sequence of integer IDs called tokens.

Tokenization is the process that maps raw text to those integer IDs.

```
Input text:   "Platform engineers build AI platforms."
Tokens:       ["Platform", " engineers", " build", " AI", " platforms", "."]
Token IDs:    [12107, 12604, 1382, 15068, 15108, 13]
```

The exact tokenization depends on the tokenizer trained with the model. Different model families use different tokenizers and different vocabulary sizes. GPT-4 family models use a vocabulary of roughly 100,000 tokens. Llama 3 family models use around 128,000. Gemma uses 256,000.

## How Tokens Relate to Text

A rough approximation for English: one token is about 0.75 words, or approximately 4 characters.

That approximation breaks quickly in practice:

- Code is often tokenized more granularly than prose
- Some programming languages tokenize worse than others
- Non-Latin scripts can tokenize far less efficiently
- Whitespace, punctuation, and numbers have irregular patterns

An `{"id": 12345, "status": "ok"}` JSON fragment might take 12–15 tokens even though it looks short.

## Why Token Counts Matter Operationally

### Billing

Hosted model APIs charge per token. Both input tokens and output tokens count. A system prompt that is 2,000 tokens long gets charged every time it appears in a request.

Knowing how your prompts tokenize directly determines cost at scale.

### Context Window Limits

Models have a maximum context window measured in tokens. This is the total sum of input tokens plus output tokens for a single inference call.

| Model family | Approximate window |
|---|---|
| GPT-3.5 | 4,096 or 16,385 |
| GPT-4o | 128,000 |
| Claude 3.5 | 200,000 |
| Llama 3.1 70B | 128,000 |
| Mistral 7B | 32,768 |

When a request exceeds the context window, it must be rejected, truncated, or split into multiple calls. That is a design constraint, not only a warning.

### Memory Consumption

During inference, every token in the context requires memory for the key-value (KV) cache. The KV cache stores intermediate attention states so the model does not recalculate them for every generated token.

Larger context windows mean larger KV caches. Longer requests consume more GPU memory and leave less capacity for serving concurrent requests.

## Context Window Growth Trends

Context windows have grown dramatically. The platform trade-off is that large context windows do not come for free:

- They increase per-request memory pressure
- They slow TTFT for very long inputs
- They tempt application developers to stuff enormous prompts instead of designing proper retrieval

A 128K context window is available in many models. That does not mean every request should use 128K tokens.

## Platform Implications

### Prompt Budget Management

Production systems benefit from explicit prompt budgets:

```
system_prompt:       600 tokens
retrieved_context:   2,000 tokens
conversation_history: 500 tokens
user_turn:           100 tokens
output_reserve:      500 tokens
─────────────────────────────────
Total budget:        3,700 tokens
```

When any segment grows unexpectedly, truncation logic must handle it safely.

### Accurate Cost Estimation

Token counting before sending a request requires either using the model provider's counting API or running the same tokenizer locally.

For OpenAI-family models, the `tiktoken` library provides the same tokenizer client-side. For most open-weight models, the `transformers` library tokenizer can count tokens without running inference.

### Monitoring Token Usage

Every inference response includes token usage metadata:

```json
{
  "usage": {
    "prompt_tokens": 843,
    "completion_tokens": 142,
    "total_tokens": 985
  }
}
```

Platforms should capture this in every request log. Unexplained token growth is often the first signal of a prompt regression or runaway context accumulation.

### Chunking Decisions

Token awareness informs how documents are split for retrieval. Chunk sizes that look reasonable in word count may exceed or fall short of their intended token budget when measured correctly.

## Summary

| Concept | Platform Implication |
|---|---|
| Tokens are not words | Estimate token counts; do not guess |
| Input tokens drive cost | System prompts and context are not free |
| Context windows are hard limits | Requests exceeding the window must be handled |
| KV cache uses GPU memory | Long contexts reduce concurrency capacity |
| Output tokens add to cost | Max token limits protect against runaway generation |
