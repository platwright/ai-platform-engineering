# Project 03 - RAG As A Service

## Goal

Expose document ingestion and managed retrieval as a reusable platform capability instead of forcing every application team to build its own local RAG workflow.

This project turns the local sample-rag engine into a small platform service with service registration, ingestion, tenant-aware query endpoints, and reusable configuration.

## What You Will Build

- a managed service catalog for RAG services
- a CLI and HTTP API for service creation, ingestion, querying, and deletion
- per-service tenant isolation backed by explicit index files
- query run artifacts for inspection and platform debugging

## Why This Project Matters

Project 03 is where the course starts treating retrieval as a platform product. The important shift is from "my app has RAG" to "the platform offers RAG as a service." That changes ownership, contracts, and operational responsibilities.

## Project Files

- `app.py`: CLI entry point and HTTP API
- `config/app.example.json`: platform configuration
- `state/`: service catalog and generated index files
- `runs/`: generated query artifacts

## Documentation

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Quick Start

Create a service:

```bash
python projects/project-03-rag-platform/app.py create-service --service-name team-a-kb --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

Ingest its documents:

```bash
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

Query it:

```bash
python projects/project-03-rag-platform/app.py query --service-name team-a-kb --question "How should platform teams think about retrieval freshness?"
```

## Relationship To Module 09

This project is the executable companion to [modules/09-rag-platform/README.md](../../modules/09-rag-platform/README.md). It builds directly on the sample-rag engine but packages it as a managed capability.