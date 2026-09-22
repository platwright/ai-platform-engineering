# Module 10 Lab

## Goal

Run the local agent platform against the RAG platform and AI gateway, then observe tool selection, approval gating, and run artifacts.

## Step 1 - List The Available Tools

```bash
python projects/project-04-agent-platform/app.py list-tools
```

## Step 2 - Make Sure A RAG Service Exists

```bash
python projects/project-03-rag-platform/app.py create-service --service-name team-a-kb --tenant team-a --docs-dir applications/sample-rag/example-docs/team-a
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

## Step 3 - Run A Safe Objective

```bash
python projects/project-04-agent-platform/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

## Step 4 - Test Approval Gating

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb
```

This should be blocked without approval.

## Step 5 - Optional Approved Path

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb --approval-token approved:delete-rag-service
```

## Step 6 - Optional Full Stack

```bash
docker compose -f platform/docker/agent-platform-stack.compose.yml up --build
```

## Step 7 - Reflection

Write down:

- which parts of the tool surface need stronger authorization in production
- which agent state should be retained versus discarded
- which additional approval gates you would add first