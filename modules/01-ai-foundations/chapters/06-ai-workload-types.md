# Chapter 1.6 - AI Workload Types

## Why Workload Taxonomy Matters

If you deploy every AI workload the same way, you will overpay in some places and under-serve reliability in others. Workload taxonomy is a platform design tool.

## Training

Purpose: create or update model artifacts.

Operational profile:

- long running
- batch oriented
- compute heavy
- checkpoint dependent

## Fine-Tuning

Purpose: adapt a base model to a narrower task or domain.

Operational profile:

- training-like, but usually smaller in scope than pretraining
- artifact versioning required
- evaluation and rollback still necessary

## Batch Inference

Purpose: process many inputs offline.

Examples:

- support ticket classification
- nightly summarization
- document enrichment

Operational profile:

- asynchronous
- queue or job based
- throughput focused

## Online Inference

Purpose: serve user-facing or application-facing requests in real time.

Examples:

- chat completion
- extraction on form submission
- real-time moderation

Operational profile:

- synchronous
- latency sensitive
- user experience coupled

## Embedding Generation

Purpose: produce vector representations.

Operational profile:

- often asynchronous for ingestion
- sometimes synchronous for query-time retrieval
- storage coupled to vector indexes

## RAG

Purpose: retrieve relevant context before generation.

Operational profile:

- combines retrieval with inference
- depends on ingestion quality
- introduces extra latency hops
- adds vector storage and permissions concerns

## Agents

Purpose: use a model in a loop with tools, state, or control logic.

Operational profile:

- multi-step
- tool and policy aware
- harder to observe than single requests
- riskier in terms of unintended actions

## Multimodal Inference

Purpose: process or generate across multiple content types such as text, audio, and images.

Operational profile:

- payload size can grow sharply
- preprocessing pipelines matter more
- storage and bandwidth needs change

## Platform Takeaway

Different workload types should lead to different assumptions about:

- compute shape
- concurrency
- storage
- failure handling
- observability
- cost models