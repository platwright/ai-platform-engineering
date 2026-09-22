# Project 04 Lab

## Goal

Run the local agent platform against Project 03 and the AI gateway, then observe how policy and approval affect execution.

## Step 1 - List Tools

```bash
python projects/project-04-agent-platform/app.py list-tools
```

## Step 2 - Run A Safe Query Objective

```bash
python projects/project-04-agent-platform/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

## Step 3 - Inspect The Run Artifact

Look at:

- planned steps
- tools called
- tool outputs
- final response

## Step 4 - Test Approval Gating

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb
```

This should not complete successfully without approval.

## Step 5 - Optional Approved Destructive Path

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb --approval-token approved:delete-rag-service
```