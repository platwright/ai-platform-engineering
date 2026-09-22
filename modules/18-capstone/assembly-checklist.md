# Capstone Assembly Checklist

Complete each section in order. Record your observations in `my-solutions/capstone-assembly.md`.

---

## Layer 1: Model API (Project 01)

```bash
python projects/project-01-model-api/app.py serve
```

Verify:
- [ ] Server starts without errors
- [ ] `GET http://localhost:8001/providers` returns a list of providers
- [ ] `POST http://localhost:8001/api/chat` with provider `acme-fast` returns a response
- [ ] Response includes a `usage` field with `prompt_tokens` and `completion_tokens`
- [ ] A run artifact was written to `projects/project-01-model-api/runs/`

Observation to record: What is the token count for a typical response? What does this imply about cost at 10,000 requests/day?

---

## Layer 2: Sample Chat Application

In a second terminal:
```bash
python applications/sample-chat/app.py serve
```

Verify:
- [ ] Application starts and reports a listening port
- [ ] `POST http://localhost:8080/api/chat` returns a response
- [ ] The response text is different from a raw Project 01 call (system prompt applied)
- [ ] Stopping Project 01 causes sample-chat to return a meaningful error (not a crash)

Observation to record: What does the sample-chat system prompt add? Is that difference visible in the response?

---

## Layer 3: Docker Compose Stack (Module 04)

Stop the individual processes and start the Compose stack:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml up --build
```

Verify:
- [ ] Both services start without errors
- [ ] `GET http://localhost:8080/health` returns successfully
- [ ] `POST http://localhost:8080/api/chat` returns a response
- [ ] `docker compose logs` shows request activity from both services

Observation to record: What changed about the startup behavior compared to running processes directly? What would need to change to run this in a real container registry?

---

## Layer 4: AI Gateway (Module 08)

Stop the previous stack and start the gateway stack:

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml up --build
```

Verify:
- [ ] Gateway starts and logs indicate it is listening
- [ ] `POST http://localhost:8080/api/chat` reaches a model via the gateway
- [ ] Gateway logs show a route selection event
- [ ] `GET http://localhost:8080/health` returns healthy

Observation to record: What routing decision did the gateway make? What would trigger the fallback path?

---

## Layer 5: RAG Platform (Module 09 / Project 03)

```bash
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a

python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb

python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is retrieval freshness?"
```

Verify:
- [ ] Service creation succeeds
- [ ] Ingestion produces a state file in `projects/project-03-rag-platform/state/`
- [ ] Query returns a response with retrieved context
- [ ] Query run artifact is written to `projects/project-03-rag-platform/runs/`

Observation to record: How many chunks were retrieved? What does the response tell you about retrieval quality?

---

## Layer 6: Agent Platform (Module 10 / Project 04)

```bash
python projects/project-04-agent-platform/app.py list-tools

python projects/project-04-agent-platform/app.py run \
  --objective "Explain retrieval freshness for the team-a knowledge base" \
  --service-name team-a-kb

python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" \
  --service-name team-a-kb
```

Verify:
- [ ] `list-tools` returns the available tool catalog
- [ ] Safe objective runs successfully and returns a response
- [ ] Destructive objective is blocked without an approval token
- [ ] Run artifacts are written for both runs

Observation to record: What tools were called during the safe run? What did the blocked run artifact contain?

---

## Layer 7: Evaluation Pipeline (Module 11)

```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

Verify:
- [ ] Eval runner executes without errors
- [ ] Per-case scores are printed
- [ ] An aggregate pass rate is reported
- [ ] Exit code is 0 if passing, 1 if failing

Observation to record: What was the pass rate? What does the lowest-scoring case tell you about the RAG pipeline?

---

## Layer 8: Security Posture Review

```bash
# Check for any literal API keys in tracked config files
git grep -i "api_key\|sk-\|bearer" -- "*.json" "*.yaml" "*.yml" "*.env"
```

Verify:
- [ ] No real API keys appear in tracked files
- [ ] All config files use placeholders or environment variable references
- [ ] Project 04 approval gate blocks unauthorized destructive actions (verified in Layer 6)
- [ ] RAG tenant isolation holds (team-a queries cannot return team-b documents if two tenants exist)

Observation to record: What is the biggest security gap in the current local implementation?

---

## Layer 9: Cost Attribution

```bash
python eval/cost_report.py
```

Verify:
- [ ] Script produces a cost summary from run artifacts
- [ ] At least one provider appears in the breakdown
- [ ] A projected monthly cost is shown

Observation to record: At the current request rate, what would this platform cost per month using real model pricing?

---

## Layer 10: Developer Portal Entry

Open `platform/backstage/catalog/ai-gateway.yaml` (created in Module 17 lab).

Verify:
- [ ] File exists and is valid YAML
- [ ] It correctly identifies the AI gateway component, its owner, and its API
- [ ] A RAG platform catalog entry also exists

Observation to record: What would a new developer learn about the platform from these catalog entries that they could not learn from source code alone?

---

## Assembly Complete

When all ten layers are verified, record in `my-solutions/capstone-assembly.md`:

1. Total time to assemble the full stack from scratch: _____ minutes
2. The step that took the longest and why
3. The step where you encountered a problem and how you resolved it
4. One thing you would change to reduce assembly time for the next engineer
