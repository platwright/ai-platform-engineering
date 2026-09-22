# Sample RAG Application

## Goal

Provide a small local-first RAG application that makes ingestion, chunking, retrieval, reranking, and grounded generation visible as separate concerns.

This application is intentionally simple. It exists so Module 09 can teach RAG as a reusable platform capability rather than as a vague chatbot pattern.

## What It Does

- ingests local documents into a tenant-aware chunk index
- creates lightweight hashed-vector representations for local retrieval practice
- retrieves and reranks relevant chunks for a question
- sends grounded prompts to the AI gateway or another compatible backend endpoint
- stores query run artifacts for inspection

## Files

- `app.py`: CLI entry point and local server launcher
- `config/app.example.json`: application and retrieval configuration
- `example-docs/`: tenant-scoped sample documents for ingestion
- `state/`: generated local index files
- `runs/`: generated query artifacts

## Quick Start

Ingest the example documents for one tenant:

```bash
python applications/sample-rag/app.py ingest --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

Query the local index:

```bash
python applications/sample-rag/app.py query --tenant team-a --question "How should platform teams think about retrieval freshness?"
```

The query path expects the local AI gateway from Module 08 to be running by default.

## Why It Matters

This application is the bridge from a single AI endpoint to a reusable retrieval capability.

- Module 08 uses a shared gateway as the stable model access layer.
- Module 09 uses this app to show that RAG requires ingestion, storage, retrieval, and operational boundaries.

## Notes

- Generated state and run artifacts are ignored by Git.
- The local embedding method is a lightweight course approximation, not a replacement for production embedding models.