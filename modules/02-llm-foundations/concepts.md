# Module 02 Concepts

## Tokens Are the Unit of Everything

LLMs do not see characters or words. They see tokens. Token counts determine cost, capacity, and context window usage. One approximate rule: 1 token ≈ 0.75 English words ≈ 4 characters. This approximation fails for code, non-Latin scripts, and numbers. Always measure rather than estimate.

## Context Window Is a Hard Constraint

The context window is the total number of tokens a model can process in a single inference call, combining input and output. Exceeding it causes failures or silent truncation. KV cache memory scales with context length, which means long contexts reduce serving concurrency.

## Generation Parameters Control Output Behavior

Temperature controls randomness. Top-p controls the sampling vocabulary. Max tokens caps output length. These are not optional tuning knobs — they are runtime contracts that affect reproducibility, cost, and quality. Production defaults should be documented and version-controlled.

## Structured Outputs Are Contracts

JSON mode produces syntactically valid JSON. Schema-constrained generation produces JSON matching a specific schema. Neither eliminates semantic errors. Validation must happen in the calling layer. Structured output schemas evolve and need versioning just like API schemas.

## Tool Calling Is an Authorization Surface

When a model can call tools, every tool is a potential attack vector. The platform must define which agents can invoke which tools, log every invocation, sandbox execution, and require explicit approval for destructive or side-effecting operations. Tool descriptions are the model's only guide to correct usage — poor descriptions produce incorrect calls.

## Streaming Changes Infrastructure Requirements

Streaming reduces time to first token at the cost of requiring long-lived connections through every intermediary. Proxies, gateways, and load balancers must all support chunked transfer without buffering. Latency now splits into TTFT and generation rate, both of which need separate observability.

## Hosted Versus Self-Hosted Is a Continuous Decision

Hosted APIs offer simplicity but create cost, privacy, and dependency risks at scale. Self-hosted models offer control and predictable cost but create operational burden. Most mature platforms route across both based on sensitivity, cost, and capability requirements. The decision should be revisited as volumes and model capabilities change.
