# Final AI Platform — Operational Runbook

Quick reference for diagnosing and resolving common platform incidents.

---

## Runbook Index

| Incident | Section |
|---|---|
| Gateway returns 5xx | [Gateway Errors](#gateway-errors) |
| Responses are slow (TTFT high) | [High Latency](#high-latency) |
| Response quality degraded | [Quality Degradation](#quality-degradation) |
| RAG returns no results | [RAG Zero Results](#rag-zero-results) |
| RAG index is stale | [RAG Index Staleness](#rag-index-staleness) |
| Agent blocked unexpectedly | [Agent Authorization](#agent-authorization) |
| Cost spike | [Cost Spike](#cost-spike) |
| Container crash / OOM | [Container Recovery](#container-recovery) |

---

## Gateway Errors

**Symptoms**: HTTP 5xx from the gateway, users cannot get responses.

**Step 1 — Check upstream provider**
```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml logs ai-gateway | tail -50
# Look for: upstream timeout, provider error, connection refused
```

**Step 2 — Check Project 01**
```bash
curl -s http://localhost:8001/providers
# If this fails: Project 01 is down
```

**Step 3 — Restart if needed**
```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml restart ai-gateway
```

**Recovery check**: `curl -s http://localhost:8080/health`

---

## High Latency

**Symptoms**: TTFT > 3 seconds, users reporting "slow" responses.

**Step 1 — Time a request manually**
```bash
time curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi"}' > /dev/null
```

**Step 2 — Identify where time is spent**
```bash
# Check if it is the RAG retrieval step
time python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb --question "test" > /dev/null
```

**Step 3 — Check for prompt length growth**
- Open recent run artifacts and compare `prompt_tokens` to baseline
- Token count above 3,000 suggests context or system prompt is growing

**Recovery**: reduce system prompt length, trim retrieved context, or check for context accumulation in conversational paths.

---

## Quality Degradation

**Symptoms**: Responses feel different, users report wrong or irrelevant answers, eval score dropped.

**Step 1 — Run evaluation**
```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

**Step 2 — Check recent changes**
- Was a prompt changed recently? Check `git log prompts/`
- Was the model version changed?
- Is the RAG index stale? (check index file modification time)

**Step 3 — Identify failing eval cases**
- The eval runner prints per-case results
- Focus on cases that previously passed and now fail

**Recovery**:
- Prompt regression: `git revert` the prompt change
- Stale index: re-ingest (`python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb`)
- Model drift: repin model version in config

---

## RAG Zero Results

**Symptoms**: RAG query returns empty or very short context.

**Step 1 — Verify the index exists**
```bash
ls -la projects/project-03-rag-platform/state/
# Expect: team-a-kb.json present
```

**Step 2 — Re-ingest if missing**
```bash
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

**Step 3 — Test a simple query**
```bash
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is retrieval freshness?"
```

**Recovery check**: response includes retrieved chunks in the output.

---

## RAG Index Staleness

**Symptoms**: Responses reference outdated information, index modification timestamp is old.

**Check staleness**:
```bash
# Linux/macOS
stat projects/project-03-rag-platform/state/team-a-kb.json

# Windows
(Get-Item projects/project-03-rag-platform/state/team-a-kb.json).LastWriteTime
```

**Re-ingest**:
```bash
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

**Prevention**: for production, set up a scheduled ingest job and alert when `index_age > 24h`.

---

## Agent Authorization

**Symptoms**: Agent blocks a request that should succeed, or approval gate fails unexpectedly.

**Step 1 — Check the run artifact**
```bash
ls -lt projects/project-04-agent-platform/runs/ | head -5
cat projects/project-04-agent-platform/runs/<latest>.json | python -m json.tool
# Look for: authorized, blocked_reason, approval_status fields
```

**Step 2 — Verify the tool is in scope**
```bash
python projects/project-04-agent-platform/app.py list-tools
# Confirm the tool you expect is listed
```

**Step 3 — Test with approval token for destructive actions**
```bash
python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" \
  --service-name team-a-kb \
  --approval-token approved:delete-rag-service
```

---

## Cost Spike

**Symptoms**: Token usage or cost metrics are significantly higher than baseline.

**Step 1 — Generate a cost report**
```bash
python eval/cost_report.py
# Compare to the previous run
```

**Step 2 — Check for prompt length growth**
- Open recent run artifacts and compare `prompt_tokens` to typical baseline
- A prompt_tokens increase of > 50% without corresponding user message length increase is a regression

**Step 3 — Check for eval or batch jobs**
- Eval pipeline running unexpectedly?
- Batch processing job not rate-limited?

**Recovery**: identify the root cause change, revert if it is a regression, add `max_tokens` limits if output is growing unconstrained.

---

## Container Recovery

**Symptoms**: Container exit, Docker Compose reports unhealthy, OOM in logs.

**Check status**:
```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml ps
docker compose -f platform/docker/ai-gateway-stack.compose.yml logs --tail=50
```

**Restart**:
```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml restart
```

**Check for OOM**:
```bash
docker inspect $(docker compose ps -q ai-gateway) | grep -A5 '"OOMKilled"'
```

If OOM: reduce `--max-num-seqs` in vLLM serving config, or add more memory to the container limit.

---

## Escalation

For incidents not resolved by this runbook:

1. Capture full logs: `docker compose logs > incident-logs-$(date +%Y%m%d).txt`
2. Capture run artifacts from the failing path
3. Record the exact command sequence that reproduced the issue
4. Post in the team channel with the above artifacts attached
