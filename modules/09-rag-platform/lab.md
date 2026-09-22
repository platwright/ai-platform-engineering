# Module 09 Lab

## Goal

Ingest tenant-scoped documents, retrieve relevant chunks, rerank them, and send grounded context through the AI gateway.

## Step 1 - Ingest The Example Documents

```bash
python applications/sample-rag/app.py ingest --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

## Step 2 - Query The Local Index

```bash
python applications/sample-rag/app.py query --tenant team-a --question "How should platform teams think about retrieval freshness?"
```

This expects the local AI gateway from Module 08 to be running by default.

## Step 3 - Inspect The Query Artifact

Open the generated JSON report and look at:

- retrieved chunks
- selected reranked chunks
- backend response metadata
- error or success state

## Step 4 - Compare Tenant Behavior

Ingest another tenant and compare:

```bash
python applications/sample-rag/app.py ingest --tenant team-b --docs-dir applications/sample-rag/example-docs/team-b
```

Ask a question that belongs to `team-a` and confirm that the query still uses only the requested tenant's index.

## Step 5 - Reflection

Write down:

- where freshness could fail
- where multi-tenant isolation could fail
- what a future managed RAG platform should add beyond this local example