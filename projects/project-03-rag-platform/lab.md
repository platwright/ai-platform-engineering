# Project 03 Lab

## Goal

Create a managed RAG service, ingest documents into it, and query it through a stable service interface.

## Step 1 - Create A Service

```bash
python projects/project-03-rag-platform/app.py create-service --service-name team-a-kb --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
```

## Step 2 - List Services

```bash
python projects/project-03-rag-platform/app.py list-services
```

## Step 3 - Ingest The Documents

```bash
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

## Step 4 - Query The Service

```bash
python projects/project-03-rag-platform/app.py query --service-name team-a-kb --question "How should platform teams think about retrieval freshness?"
```

## Step 5 - Optional HTTP API Path

Start the service:

```bash
python projects/project-03-rag-platform/app.py serve
```

Then create or query services over HTTP.