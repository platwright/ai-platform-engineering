# Failure Lab: Stale RAG Index

**Covers**: Module 09 (RAG Platform), Module 14 (Reliability), Module 11 (LLMOps)

**Difficulty**: Intermediate

**Estimated time**: 45–60 minutes

---

## Objective

Simulate a RAG index staleness scenario: update source documents after ingestion and observe how query quality degrades without causing any HTTP error. Build a detection signal that would catch this failure in production.

---

## Prerequisites

- Project 01 and Project 03 working locally
- The `team-a-kb` service ingested with the default example documents
- Module 09 and Module 11 material reviewed

---

## Step 1: Setup — Establish A Baseline

Ingest the example documents and record baseline query quality:

```bash
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a

python projects/project-03-rag-platform/app.py ingest \
  --service-name team-a-kb

python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is retrieval freshness?"
```

Note the response. It should include content from the example documents.

Also record the index modification timestamp:

```bash
# Linux/macOS
stat projects/project-03-rag-platform/state/team-a-kb-index.json

# Windows PowerShell
(Get-Item projects/project-03-rag-platform/state/team-a-kb-index.json).LastWriteTime
```

---

## Step 2: Create The Failure Condition — Update Source Documents

Create an updated version of the source document that contains new information:

```bash
# Add a new document with information that was NOT in the original index
cat > /tmp/new-knowledge.txt << 'EOF'
Retrieval freshness policy update (Q4 2025):
All RAG indexes must be refreshed within 4 hours of source document changes.
Stale indexes older than 24 hours trigger automatic quality alerts.
The new freshness SLO requires index age to stay below 12 hours for production tenants.
EOF

cp /tmp/new-knowledge.txt applications/sample-rag/example-docs/team-a/freshness-policy-update.txt
```

**Important**: Do NOT re-ingest yet. The index is now stale — the new document exists on disk but is not in the index.

---

## Step 3: Observe The Symptoms

Query for the new information:

```bash
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is the new freshness SLO for production tenants?"
```

Observe:
- Does the response return an HTTP error? (It should not)
- Does the response reference the new freshness SLO? (It should not — the new document is not indexed)
- Is the response confidently wrong, or does it say it doesn't know?
- Is there any signal in the application output that the index is stale?

Record your observations in `my-notes/failure-lab-staleness.md`.

---

## Step 4: Diagnose — Index Age Check

There is no automatic staleness signal in the current implementation. You must check manually:

```bash
# Check when the index was last updated
python projects/project-03-rag-platform/app.py describe \
  --service-name team-a-kb
```

Or check the index file directly:

```bash
python -c "
import json
from pathlib import Path

index = json.loads(Path('projects/project-03-rag-platform/state/team-a-kb-index.json').read_text())
tenants = index.get('tenants', {})
for tenant, data in tenants.items():
    print(f'Tenant: {tenant}')
    print(f'Updated at: {data.get(\"updated_at\", \"unknown\")}')
    print(f'Chunks: {len(data.get(\"chunks\", []))}')
"
```

Questions to answer:
1. How would you detect this failure from outside the platform (as an application team)?
2. How old is the index right now?
3. What is the index age at which you would want an alert to fire?

---

## Step 5: Recovery — Re-Ingest

Restore correct behavior by re-ingesting the updated documents:

```bash
python projects/project-03-rag-platform/app.py ingest \
  --service-name team-a-kb
```

Re-run the query:

```bash
python projects/project-03-rag-platform/app.py query \
  --service-name team-a-kb \
  --question "What is the new freshness SLO for production tenants?"
```

Confirm the new document now appears in the retrieved context.

---

## Step 6: Build A Detection Signal

Write a Python script at `labs/failure-labs/rag-staleness/check_staleness.py` that:

1. Reads all index files from `projects/project-03-rag-platform/state/`
2. Reports the age of each index in hours
3. Exits with code 1 if any index is older than a configurable threshold (default: 24 hours)

```python
#!/usr/bin/env python3
"""
Check RAG index staleness across all services.
Exits with code 1 if any index exceeds the max age threshold.

Usage:
    python check_staleness.py                     # 24-hour default threshold
    python check_staleness.py --max-age-hours 4   # custom threshold
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def check_staleness(state_dir: Path, max_age_hours: float) -> list[dict]:
    violations = []
    for path in sorted(state_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        for tenant, tdata in data.get("tenants", {}).items():
            updated_at = tdata.get("updated_at")
            if not updated_at:
                violations.append({"service": path.stem, "tenant": tenant,
                                    "age_hours": None, "issue": "missing updated_at"})
                continue
            updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - updated_dt).total_seconds() / 3600
            status = "STALE" if age_hours > max_age_hours else "OK"
            print(f"[{status}] {path.stem} / {tenant}: {age_hours:.1f}h old")
            if age_hours > max_age_hours:
                violations.append({"service": path.stem, "tenant": tenant,
                                    "age_hours": round(age_hours, 1)})
    return violations


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check RAG index staleness")
    parser.add_argument("--state-dir",
                        default="projects/project-03-rag-platform/state")
    parser.add_argument("--max-age-hours", type=float, default=24.0)
    args = parser.parse_args()

    violations = check_staleness(Path(args.state_dir), args.max_age_hours)
    if violations:
        print(f"\n{len(violations)} stale index(es) found.")
        sys.exit(1)
    print("\nAll indexes are within the freshness threshold.")
```

Run it against your current state:

```bash
python labs/failure-labs/rag-staleness/check_staleness.py --max-age-hours 0.1
```

---

## Step 7: Prevention

In `my-notes/failure-lab-staleness.md`, describe:

1. How would you integrate `check_staleness.py` into a CI pipeline?
2. What Prometheus metric would you expose from the RAG platform to make index age observable?
3. Describe a scenario where automatic re-ingestion would be dangerous (hint: think about document authorization).
4. What is the difference between a stale index causing a quality failure and a missing index causing an error? Which is harder to detect?

---

## Expected Outcomes

| Observation | Expected |
|---|---|
| Query for new content returns HTTP 200 | Yes — no error code |
| Response does not contain the new content | Yes — silent quality failure |
| Index age is detectable from state file | Yes — `updated_at` field |
| Re-ingestion restores correct responses | Yes |
| Staleness checker exits 1 on stale index | Yes |

---

## Cleanup

Remove the temporary document:

```bash
rm applications/sample-rag/example-docs/team-a/freshness-policy-update.txt
```

Re-ingest to restore the original index:

```bash
python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```
