# Chapter 0.2 - What We Will Build

## Central Narrative

The course follows a fictional company called Acme AI. Several teams want AI features, but they should not each solve model access, retrieval, observability, secrets, and policy in different ways.

The answer is an internal AI platform.

## Stage 1 - Application To Model API

The first useful shape is simple: one application calling one model API. This is enough to introduce inference behavior, latency, cost, tokens, and failure handling.

## Stage 2 - Application To AI Gateway To Models

Once more than one provider or model appears, the organization needs a gateway for routing, credentials, quotas, fallback, and usage tracking.

## Stage 3 - Application To Gateway To RAG To Model

Applications now need document-aware responses, which introduces ingestion, chunking, embeddings, retrieval, and context assembly.

## Stage 4 - Agents To Tools Or MCP To Models

Some workloads move beyond single-shot generation. Agents introduce tool execution, control loops, memory, safety boundaries, and new observability requirements.

## Stage 5 - Kubernetes, GPUs, And Model Serving

At this point the platform may need self-hosted models, better runtime controls, and GPU-backed serving infrastructure.

## Stage 6 - Observability, Evaluations, And Security

The platform is not production-grade until teams can trace behavior, compare changes, secure access, and enforce policy.

## Stage 7 - Developer Self-Service

Eventually the platform should expose templates, APIs, and paved roads so application teams can ship without deep platform knowledge.

## Why The Narrative Matters

This sequencing prevents the course from becoming a set of disconnected demos. Each module adds another layer to the same platform so the learner can reason about integration points and tradeoffs.