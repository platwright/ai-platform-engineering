# Final AI Platform — Deployment Guide

This guide deploys the complete local platform from scratch. Estimated time: 30–60 minutes on first run, 10–15 minutes on subsequent runs.

## Prerequisites

Run the environment check first:

```bash
./scripts/setup/check-prereqs.sh   # Linux/macOS
./scripts/setup/check-prereqs.ps1  # Windows PowerShell
```

Required: Python 3.11+, Docker, Docker Compose.
Optional for Kubernetes layers: kubectl, kind or k3d, Helm.

---

## Phase 1: Model API Layer

**Start Project 01:**

```bash
# Copy config if not done yet
cp projects/project-01-model-api/config/app.example.json \
   projects/project-01-model-api/config/app.json

# Start the model API server
python projects/project-01-model-api/app.py serve
```

**Verify (in a new terminal):**

```bash
curl -s http://localhost:8001/providers | python -m json.tool
# Expect: list of configured providers

curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "provider": "acme-fast"}' | python -m json.tool
# Expect: JSON with response and usage fields
```

---

## Phase 2: Application Layer

**Start sample-chat (in a new terminal, with Phase 1 running):**

```bash
cp applications/sample-chat/config/app.example.json \
   applications/sample-chat/config/app.json

python applications/sample-chat/app.py serve
```

**Verify:**

```bash
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the role of an AI gateway?"}' | python -m json.tool
```

---

## Phase 3: Docker Compose Stack

Stop individual processes (Ctrl+C). Use Compose for all-in-one startup:

```bash
# Build and start
docker compose -f platform/docker/ai-gateway-stack.compose.yml up --build -d

# Check health
curl -s http://localhost:8080/health
docker compose -f platform/docker/ai-gateway-stack.compose.yml ps
```

**Verify gateway routing:**

```bash
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain AI gateway routing."}' | python -m json.tool
```

---

## Phase 4: RAG Platform

With the gateway stack running:

```bash
# Initialize sample RAG data
cp projects/project-03-rag-platform/config/app.example.json \
   projects/project-03-rag-platform/config/app.json

# Create tenant services
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb \
  --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a

python projects/project-03-rag-platform/app.py ingest \
  --service-name team-a-kb
```

**Verify:**

```bash
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is retrieval freshness?"
# Expect: response with retrieved context
```

---

## Phase 5: Agent Platform

```bash
cp projects/project-04-agent-platform/config/app.example.json \
   projects/project-04-agent-platform/config/app.json

# Verify tool list
python projects/project-04-agent-platform/app.py list-tools

# Test safe run
python projects/project-04-agent-platform/app.py run \
  --objective "Explain retrieval freshness for the team-a knowledge base" \
  --service-name team-a-kb

# Test approval gate
python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" \
  --service-name team-a-kb
# Expect: blocked without approval token
```

---

## Phase 6: Full Stack via Compose

For the full integrated stack:

```bash
docker compose -f platform/docker/agent-platform-stack.compose.yml up --build -d
```

This starts the gateway, RAG service, and agent platform together.

---

## Phase 7: Evaluation Pipeline

```bash
# Create eval dataset if not present
mkdir -p eval/datasets
# (Use the dataset from Module 11 lab, or create eval/datasets/rag-smoke.json)

python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

---

## Phase 8: Cost Report

```bash
python eval/cost_report.py
# Expect: per-provider cost breakdown from run artifacts
```

---

## Phase 9: Developer Portal

```bash
cd platform/backstage

# First time only
npm install

# Start Backstage
npm run dev
# Portal available at http://localhost:3000
```

Load catalog entries:
- `platform/backstage/catalog/ai-gateway.yaml`
- `platform/backstage/catalog/rag-platform.yaml`

---

## Full-Platform Health Check

With all phases running:

```bash
# Model API
curl -s http://localhost:8001/providers > /dev/null && echo "Model API: OK"

# Gateway
curl -s http://localhost:8080/health > /dev/null && echo "Gateway: OK"

# RAG
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb --question "test" > /dev/null && echo "RAG: OK"

# Agent
python projects/project-04-agent-platform/app.py list-tools > /dev/null && echo "Agents: OK"

echo "Platform health check complete."
```

---

## Teardown

```bash
# Stop Compose stacks
docker compose -f platform/docker/agent-platform-stack.compose.yml down
docker compose -f platform/docker/ai-gateway-stack.compose.yml down

# Clean state (preserves config)
rm -rf projects/project-03-rag-platform/state/*
rm -rf projects/project-04-agent-platform/runs/*

# Full reset (also removes run artifacts)
rm -rf projects/*/runs/* applications/*/runs/*
```
