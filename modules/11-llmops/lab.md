# Module 11 Lab

## Goal

Build a minimal evaluation loop for the sample-rag application: load a test dataset, run queries through the RAG pipeline, score responses, and produce a pass/fail report.

## Prerequisites

- Project 03 (RAG platform) ingested with sample documents
- Python 3.11+
- The AI gateway or a mock provider running

## Step 1 - Create An Evaluation Dataset

Create a file at `eval/datasets/rag-smoke.json`:

```json
[
  {
    "id": "eval-001",
    "question": "What is retrieval freshness and why does it matter?",
    "expected_themes": ["freshness", "stale", "index", "update"],
    "tags": ["core"]
  },
  {
    "id": "eval-002",
    "question": "How do chunking decisions affect retrieval quality?",
    "expected_themes": ["chunk", "size", "overlap", "precision", "recall"],
    "tags": ["core"]
  },
  {
    "id": "eval-003",
    "question": "What makes a RAG pipeline a platform capability rather than an application feature?",
    "expected_themes": ["multi-tenant", "reusable", "platform", "service"],
    "tags": ["core"]
  },
  {
    "id": "eval-004",
    "question": "What are the operational signals that indicate a RAG platform is degrading?",
    "expected_themes": ["latency", "freshness", "error", "quality", "metric"],
    "tags": ["operations"]
  },
  {
    "id": "eval-005",
    "question": "Why is reranking useful after vector similarity retrieval?",
    "expected_themes": ["rerank", "similarity", "precision", "relevance"],
    "tags": ["core"]
  }
]
```

## Step 2 - Write The Eval Runner

Create `eval/run_eval.py`:

```python
#!/usr/bin/env python3
"""
Minimal evaluation runner for the RAG platform.
Runs each case through the RAG query pipeline and scores keyword coverage.
"""
import json
import subprocess
import sys

def query_rag(question: str, service_name: str) -> str:
    """Run a RAG query and return the response text."""
    result = subprocess.run(
        [
            "python", "projects/project-03-rag-platform/app.py",
            "query",
            "--service-name", service_name,
            "--question", question,
        ],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def keyword_score(response: str, themes: list[str]) -> float:
    response_lower = response.lower()
    matched = sum(1 for t in themes if t.lower() in response_lower)
    return round(matched / len(themes), 2) if themes else 0.0

def run_eval(dataset_path: str, service_name: str, threshold: float = 0.60):
    dataset = json.load(open(dataset_path))
    results = []

    for case in dataset:
        response = query_rag(case["question"], service_name)
        score = keyword_score(response, case["expected_themes"])
        passed = score >= threshold
        results.append({
            "id": case["id"],
            "question": case["question"],
            "score": score,
            "passed": passed,
            "response_preview": response[:200]
        })
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {case['id']}: score={score}")

    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    pass_rate = round(passed / total, 3)

    print(f"\nResults: {passed}/{total} passed ({pass_rate:.1%})")
    print(f"Threshold: {threshold:.1%}")
    print("OVERALL: PASS" if pass_rate >= threshold else "OVERALL: FAIL")

    return pass_rate >= threshold

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--service-name", default="team-a-kb")
    parser.add_argument("--threshold", type=float, default=0.60)
    args = parser.parse_args()

    passed = run_eval(args.dataset, args.service_name, args.threshold)
    sys.exit(0 if passed else 1)
```

## Step 3 - Make Sure A RAG Service Exists

```bash
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb \
  --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a

python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb
```

## Step 4 - Run The Evaluation

```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

The script exits with code 0 if the pass rate meets the threshold and 1 otherwise, making it suitable as a CI gate.

## Step 5 - Observe The Results

Look at the output:
- Which cases passed? Which failed?
- For failed cases, is the response missing the expected concepts or addressing them differently?
- What does this tell you about the RAG pipeline's current quality?

## Step 6 - Simulate A Regression

Edit the system prompt in `applications/sample-rag/config/app.json` to remove grounding instructions. Re-run the eval:

```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.60
```

Does the pass rate drop? Does the eval correctly detect the regression?

## Step 7 - Reflection

Write in your workbook (`my-notes/module-11.md`):

1. What categories of questions would you add to this eval dataset based on your experience with the platform?
2. What is the biggest limitation of keyword-based scoring for this use case?
3. Design a simple LLM-as-judge prompt that could replace keyword scoring for one eval case.
4. How would you integrate this eval script into a GitHub Actions pipeline?
