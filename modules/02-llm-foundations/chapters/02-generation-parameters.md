# Chapter 02 - Generation Parameters

## What Generation Parameters Are

Language models generate output by repeatedly predicting the next token given the current context. That prediction is a probability distribution over every token in the vocabulary.

Generation parameters control how the model samples from that distribution. Understanding them matters because they directly affect output behavior, reproducibility, cost, and debugging.

## Temperature

Temperature controls the sharpness of the probability distribution before sampling.

- Low temperature (< 0.5): flattens toward the highest-probability tokens, making output more deterministic and focused
- Temperature = 1.0: uses the raw model distribution without modification
- High temperature (> 1.0): sharpens toward lower-probability tokens, making output more varied and creative

```
Temperature 0.1: the model will almost always pick the most likely next word
Temperature 0.7: the model occasionally picks less common but plausible words
Temperature 1.5: the model may pick surprising or unexpected words
```

Setting `temperature=0` is a common approximation for deterministic output, but it is not truly deterministic in practice. Floating-point ordering and parallel inference can still produce minor variation.

## Top-P (Nucleus Sampling)

Top-p sampling restricts the sampling pool to the smallest set of tokens whose cumulative probability mass exceeds the threshold `p`.

- `top_p=1.0`: include all tokens (no restriction)
- `top_p=0.9`: sample only from the top 90% probability mass tokens
- `top_p=0.1`: sample from a very small set of top tokens

Top-p is typically more stable than temperature alone because the number of candidates adapts to the entropy of the distribution at each step.

Top-p and temperature are usually both applied. A common pairing is `temperature=0.7, top_p=0.9`.

## Top-K

Top-k sampling restricts sampling to the K highest-probability tokens regardless of probability mass.

- `top_k=50`: choose only from the 50 most likely next tokens
- `top_k=1`: always pick the single most likely token (greedy)

Top-k is simpler to reason about than top-p but less adaptive. Some serving systems use it as a hard backstop even when top-p is the primary strategy.

## Repetition and Frequency Penalties

### Repetition Penalty

Applies a multiplicative penalty to tokens that have already appeared in the output. Values above 1.0 reduce the likelihood of repeated tokens. Typical range: 1.0–1.2.

### Frequency Penalty

Reduces the probability of tokens in proportion to how many times they have appeared. More appearances equals a stronger penalty.

### Presence Penalty

Applies a flat penalty to any token that has appeared at least once, regardless of frequency.

### Platform Implication

Over-aggressive penalties cause model output to avoid common words unnaturally. Under-configured penalties allow looping or repetitive outputs. Both need to be tested with realistic prompts before production deployment.

## Max Tokens (Max New Tokens)

The maximum number of output tokens the model will generate in a single call.

This is a budget and safety control, not a target. The model stops when it finishes naturally or when the limit is reached, whichever comes first.

Production systems should always set a `max_tokens` limit. Unbounded generation can:

- create runaway cost on hosted APIs
- cause GPU memory pressure on self-hosted serving
- delay downstream timeout handling

A reasonable default depends on the use case:

| Use case | Typical max_tokens range |
|---|---|
| Quick factual lookup | 100–300 |
| Conversational reply | 300–800 |
| Document analysis or summary | 800–2000 |
| Code generation | 1000–4000 |
| Long-form draft | 2000–8000 |

## Stop Sequences

Stop sequences are strings that instruct the model to halt generation immediately when produced.

```json
{
  "stop": ["###", "```", "\n\nUser:"]
}
```

Stop sequences are useful for:

- structured output templates with explicit terminators
- turn-based dialog formats that should not bleed across turns
- code snippets that should stop at a certain delimiter

The model finishes the token currently in progress and then stops. Stop sequences are not guaranteed to appear in the output; they terminate and are discarded.

## Seed (Reproducibility)

Setting a `seed` value instructs the serving system to attempt deterministic sampling. Given the same seed, prompt, and parameters, the model should produce the same output.

In practice:

- Seeds improve reproducibility but do not guarantee identical results across different hardware, quantization levels, or batching configurations
- Seeds are useful for debugging, A/B testing, and evaluation
- Seeds are not a substitute for real evaluation across distribution

## Platform Implications Summary

| Parameter | Safe Default | Risk If Misconfigured |
|---|---|---|
| temperature | 0.7 for generation, 0.2 for factual tasks | Too high: unstable output. Too low: robotic or looping |
| top_p | 0.9–0.95 | Very low values degrade quality on complex prompts |
| max_tokens | Tuned per use case | Unbounded: runaway cost and latency |
| repetition_penalty | 1.1 | Too high: unnatural avoidance of common words |
| seed | Set during evaluation and testing | Omit in production for natural variation |

## Making Parameters Observable

Production serving should log generation parameters alongside every request, not just responses. When output quality regresses, the first diagnostic question is whether parameters changed.

Parameter consistency across environments also matters. Development, staging, and production should use the same generation configuration unless there is an intentional, documented reason for the difference.
