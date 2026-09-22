# Module 09 - RAG Platform

## Overview

This module treats retrieval as a reusable platform capability rather than as a one-off chatbot feature. It focuses on the full retrieval pipeline: ingestion, chunking, embedding choices, storage, query-time retrieval, reranking, multi-tenancy, and operational visibility.

The module uses the sample RAG application as a local-first implementation surface and keeps the emphasis on platform responsibilities rather than on prompt tricks.

## Learning Objectives

By the end of this module, you should be able to:

- explain why RAG exists and what problem it solves
- describe the end-to-end RAG architecture and ingestion pipeline
- compare chunking, embedding, and vector storage tradeoffs
- explain retrieval and reranking at a platform level
- reason about multi-tenant RAG boundaries and lifecycle controls
- identify the key operational signals for a RAG platform

## Prerequisites

- Completion of [modules/08-ai-gateway/README.md](../08-ai-gateway/README.md)
- Familiarity with the sample application and gateway path from earlier modules

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [Why RAG Exists](chapters/01-why-rag-exists.md)
2. [RAG Architecture](chapters/02-rag-architecture.md)
3. [Document Ingestion Pipeline](chapters/03-document-ingestion-pipeline.md)
4. [Chunking Strategies](chapters/04-chunking-strategies.md)
5. [Embedding Models](chapters/05-embedding-models.md)
6. [Vector Databases](chapters/06-vector-databases.md)
7. [Retrieval](chapters/07-retrieval.md)
8. [Reranking](chapters/08-reranking.md)
9. [Multi-Tenant RAG](chapters/09-multi-tenant-rag.md)
10. [Operating RAG](chapters/10-operating-rag.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [applications/sample-rag/README.md](../../applications/sample-rag/README.md)
- [projects/project-03-rag-platform/README.md](../../projects/project-03-rag-platform/README.md)
- [modules/08-ai-gateway/README.md](../08-ai-gateway/README.md)

## Expected Outcome

At the end of this module, you should have:

- a working local ingestion and retrieval flow
- an understanding of where retrieval quality and freshness can fail
- a clear explanation of multi-tenant isolation concerns in RAG systems
- notes on what Project 03 should provide as a reusable RAG platform service

## Knowledge Check

1. Why does RAG exist instead of only using larger prompts or a different model?
2. Why is ingestion quality as important as query-time retrieval quality?
3. How do chunking decisions affect both retrieval quality and cost?
4. What is the difference between embedding generation and retrieval itself?
5. Why is reranking useful even after retrieval already produced candidates?
6. Where can multi-tenant isolation fail in a RAG platform?
7. Which operational signals tell you that a RAG platform is degrading?

## Common Mistakes

- treating RAG as only a prompt template instead of a pipeline
- ignoring ingestion freshness and focusing only on query latency
- chunking without considering retrieval quality or context efficiency
- assuming vector similarity alone is enough for good ranking
- storing tenant data without strong metadata and access boundaries

## Production Considerations

- ingestion and retrieval paths usually need different runtime treatment
- embedding pipelines create their own cost and failure surface
- freshness, permissions, and storage growth are core platform concerns
- retrieval quality and retrieval latency must both be observed

## Next Step

Read [concepts.md](concepts.md), ingest the sample documents, and run [applications/sample-rag/README.md](../../applications/sample-rag/README.md) through [lab.md](lab.md).