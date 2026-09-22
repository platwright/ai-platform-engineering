# Module 01 Concepts

## Why This Module Exists

AI platform engineering starts with workload understanding. If you only know that an application "calls a model," you will make weak decisions about latency budgets, hardware choices, deployment patterns, observability, and cost controls.

This module gives you a platform engineer's mental model of AI systems.

## The Domain Stack

These terms are related, but not interchangeable:

- Artificial intelligence is the broad umbrella for systems that perform tasks associated with human intelligence.
- Machine learning is a subset of AI where systems learn patterns from data.
- Deep learning is a subset of machine learning based on multi-layer neural networks.
- Generative AI is a family of systems that generate new outputs such as text, images, code, audio, or video.
- Foundation models are large pre-trained models that can be adapted or prompted for many downstream tasks.
- LLMs are foundation models focused on language tasks.

## The Operational Split: Training vs Inference

Training creates model artifacts. Inference serves predictions or generated outputs from already trained artifacts.

That distinction changes nearly every infrastructure decision:

- resource profile
- workload duration
- scheduling pattern
- latency sensitivity
- storage and checkpoint strategy
- network traffic shape

## Why Parameters, Tokens, and Precision Matter

Platform teams do not need to derive the math behind transformers, but they do need to understand why runtime behavior changes when:

- parameter counts grow
- input and output tokens grow
- context windows grow
- precision changes from FP16 to INT8 or INT4
- a model is quantized or fine-tuned

## Embeddings Are Platform Work

Embeddings turn text or other content into vectors. That sounds model-centric, but operationally it introduces:

- separate embedding models
- ingestion jobs
- vector storage
- retrieval latency
- re-indexing and freshness concerns
- tenant isolation questions

## AI Workloads Are Not One Thing

An AI platform may need to support:

- long-running training jobs
- bursty online inference
- background document indexing
- periodic evaluation jobs
- retrieval pipelines
- agent tool execution loops

These patterns should not all be deployed, scaled, and observed in the same way.

## The Lifecycle Mindset

Production AI is not only about calling a model. It is about managing the full lifecycle:

- experiment
- develop
- evaluate
- package
- deploy
- serve
- observe
- improve

Every later module in this course will assume that lifecycle framing.