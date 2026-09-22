# Module 09 Concepts

## RAG Is A Platform Capability

RAG is not only a chatbot feature. It is a reusable capability made from several systems working together:

- ingestion
- chunking
- embedding generation
- vector storage
- retrieval
- reranking
- grounded generation

## Why The Pipeline Matters

Poor retrieval quality is often caused upstream. Chunking, document parsing, missing metadata, embedding failures, or stale indexes can all degrade query-time behavior.

## Multi-Tenancy Is Central

RAG platforms often serve multiple teams or products. That means tenant isolation, permissions, and lifecycle policies are platform requirements, not optional extras.

## Retrieval Has Its Own Metrics

You should care about more than answer text. Retrieval systems also need:

- ingestion success rates
- retrieval latency
- hit quality
- index freshness
- storage growth
- tenant boundary correctness

## The Local-First Constraint

The sample RAG application uses a lightweight hashed-vector approximation to keep the course runnable without external dependencies. The concepts still map to real embedding models and vector stores later.