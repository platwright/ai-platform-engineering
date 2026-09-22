# Module 12 Concepts

## AI Observability Extends MELT

The standard observability stack covers Metrics, Events, Logs, and Traces. For AI systems, each pillar needs AI-specific extensions:

- **Metrics**: add token counts, TTFT, generation rate, cache hit rate, evaluation score, GPU memory
- **Events**: add model invocations, tool calls, human approvals, prompt version changes
- **Logs**: add structured request/response records with token metadata (with privacy controls)
- **Traces**: add LLM span attributes, retrieval spans, tool execution spans

And a fifth pillar appears: **Evaluations** — quality signals that runtime telemetry cannot provide.

## Green Metrics Do Not Mean Correct Behavior

A model server can return HTTP 200 with low latency while producing hallucinated, irrelevant, or harmful outputs. Runtime metrics cannot detect quality failure. Observability for AI systems must combine operational signals (is the system up?) with quality signals (is the system correct?).

## Token Counts Drive Both Cost And Quality Signals

Token metadata appears in every LLM response. Capturing it is free. Not capturing it makes cost attribution and quality analysis impossible. Log `prompt_tokens` and `completion_tokens` for every request.

## TTFT and End-to-End Latency Are Different Problems

TTFT measures how quickly the user sees the first word. End-to-end latency measures how long until the response is complete. A model with high TTFT but fast generation produces a slow start then rapid completion. A model with low TTFT but slow generation feels responsive but takes a while to finish. Both metrics matter and they have different root causes and different fixes.

## Privacy Constrains Logging

Prompts and responses may contain PII, confidential business content, or sensitive data. You cannot log raw prompt and response content without:
- PII scrubbing or tokenization
- strict access controls on the log store
- a defined retention policy
- a legal basis for the logging under applicable privacy regulations

The decision to log full content versus only metadata should be explicit and documented.

## Distributed Traces Cross Many Service Boundaries

A single user request can touch the application, the AI gateway, the model server, the embedding service, the vector database, and the reranker. A trace that captures all of these hops provides the latency decomposition needed to diagnose complex performance problems. Without end-to-end tracing, operators guess at which layer is the bottleneck.
