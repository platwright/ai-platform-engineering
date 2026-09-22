# Project 03 Verification

## Required Checks

Create a service:

```bash
python projects/project-03-rag-platform/app.py create-service --service-name team-a-kb --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

Ingest it:

```bash
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

Query it:

```bash
python projects/project-03-rag-platform/app.py query --service-name team-a-kb --question "How should platform teams think about retrieval freshness?"
```

## Expected Result

- the service is registered in the local catalog
- ingestion succeeds and writes or updates a per-service index file
- the query returns a grounded result or a well-formed backend response if the gateway is running
- a query artifact is written under `runs/`