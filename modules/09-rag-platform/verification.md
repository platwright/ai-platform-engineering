# Module 09 Verification

## Required Checks

Ingest a tenant dataset:

```bash
python applications/sample-rag/app.py ingest --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

Run a query:

```bash
python applications/sample-rag/app.py query --tenant team-a --question "How should platform teams think about retrieval freshness?"
```

## Expected Result

- ingestion produces a local index file
- query returns a success or at least a well-formed backend result if the gateway is running
- query output includes retrieved and reranked chunk metadata

## Understanding Check

You should be able to explain:

- why RAG exists
- how chunking and embedding choices affect retrieval quality
- why reranking can improve selected context
- where multi-tenant leakage risks appear
- what platform-level metrics matter in a RAG system