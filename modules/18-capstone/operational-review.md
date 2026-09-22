# Capstone Operational Review

Complete this review against a running platform stack. Record your findings in `my-solutions/capstone-operational-review.md`.

---

## Review 1: Observability

### 1.1 - Request Logging

Send five requests through the platform and review the logs.

```bash
for i in 1 2 3 4 5; do
  python projects/project-01-model-api/app.py chat \
    --provider acme-fast \
    --message "Platform engineering question $i"
done
```

Review the run artifacts. Answer:
- Are `prompt_tokens` and `completion_tokens` logged for every request?
- Is a timestamp present?
- Is the provider/model logged?
- Would these logs be sufficient to calculate daily cost by provider?

**Rating**: Strong / Acceptable / Weak — with one-sentence justification.

### 1.2 - Quality Signal

Run the evaluation suite:

```bash
python eval/run_eval.py --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb --threshold 0.60
```

- What is the current pass rate?
- Is the pass rate above or below the 0.80 production SLO target?
- What would you do next if it were below 0.75?

**Rating**: Strong / Acceptable / Weak.

### 1.3 - Latency Visibility

Make a timed request:

```bash
time curl -s -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain token counting.", "provider": "acme-fast"}' > /dev/null
```

- Does the run artifact capture latency?
- Can you identify TTFT vs total latency?
- Do you have a p95 latency estimate?

**Rating**: Strong / Acceptable / Weak.

---

## Review 2: Security

### 2.1 - Secrets Audit

```bash
git grep -n "sk-\|api_key.*=.*[a-zA-Z0-9]{20}" -- "*.json" "*.yaml" "*.py"
```

- Are any real secrets present in tracked files?
- Are secrets referenced via environment variables or placeholders?

**Rating**: Strong / Acceptable / Weak.

### 2.2 - Approval Gate

```bash
# Should block
python projects/project-04-agent-platform/app.py run \
  --objective "Delete the team-a-kb service" --service-name team-a-kb

# Check exit code
echo "Exit code: $?"
```

- Does the destructive action block?
- Does the run artifact record the denial?

**Rating**: Strong / Acceptable / Weak.

### 2.3 - RAG Tenant Isolation

If you have two tenants ingested, verify:

```bash
# Query team-a-kb — only team-a documents should appear in retrieved context
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb --question "What do team-a documents contain?"
```

- Does the retrieved context contain only expected documents?
- Is the tenant filter applied at the storage query level or as a post-filter?

**Rating**: Strong / Acceptable / Weak.

---

## Review 3: Reliability

### 3.1 - Provider Fallback

Simulate a provider failure by using a rate-limited provider:

```bash
python projects/project-01-model-api/app.py chat \
  --provider acme-rate-limited --message "Test fallback behavior"
```

- Does the application return a meaningful error or hang?
- Is there a fallback provider configured?
- Is the failure logged?

**Rating**: Strong / Acceptable / Weak.

### 3.2 - Approval Gate Reliability

Verify the agent platform handles a missing RAG service gracefully:

```bash
# Query a non-existent service
python projects/project-04-agent-platform/app.py run \
  --objective "Query the nonexistent-kb service" --service-name nonexistent-kb
```

- Is the error message actionable?
- Does the application crash or return a structured error?

**Rating**: Strong / Acceptable / Weak.

---

## Review 4: Cost

### 4.1 - Attribution

```bash
python eval/cost_report.py
```

- Is cost attributed per provider?
- Is a projected monthly cost shown?
- Is the report actionable for a budget review?

**Rating**: Strong / Acceptable / Weak.

### 4.2 - Token Efficiency

Review a run artifact and calculate:
- What fraction of tokens are in the system prompt vs user message vs completion?
- Is there obvious token waste (very long system prompt, unnecessarily verbose output)?

**Rating**: Strong / Acceptable / Weak.

---

## Operational Review Summary

Complete in `my-solutions/capstone-operational-review.md`:

| Area | Rating | Primary Gap | First Fix |
|---|---|---|---|
| Observability | | | |
| Security | | | |
| Reliability | | | |
| Cost | | | |

**Top 3 production-readiness gaps in priority order:**

1.
2.
3.

**The most important change before moving this platform to production:**
