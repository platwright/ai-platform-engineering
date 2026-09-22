# Chapter 07 - AI CI/CD Pipelines

## How AI CI/CD Differs From Standard CI/CD

A standard CI/CD pipeline validates that code does what it claims to do: tests pass, linting is clean, the build succeeds, the artifact is deployed. The pipeline is deterministic; the same commit always produces the same result.

An AI CI/CD pipeline validates that a system produces acceptably good outputs for the inputs users actually send. The validation is probabilistic; the same change might pass on one run and fail on another due to model variance. The pipeline must be calibrated to tolerate normal variance while catching genuine regressions.

## What Changes In An AI System

Three categories of changes affect AI system behavior:

| Change Type | Risk Level | Eval Required |
|---|---|---|
| Application code (non-AI path) | Low | Standard unit tests, no eval |
| Configuration change (non-AI) | Low | Smoke test only |
| Generation parameters (temperature, max_tokens) | Medium | Smoke eval (20-50 cases) |
| Prompt change | High | Full eval suite |
| Model version change | High | Full eval suite + behavioral regression |
| RAG pipeline change | High | Full eval suite on retrieval cases |
| Routing policy change | Medium | Smoke eval + cost check |

The CI pipeline should detect which category of change occurred and trigger the appropriate level of evaluation.

## Pipeline Structure

```
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: Validate (all changes)                                 │
│   - lint prompt YAML syntax                                     │
│   - validate eval dataset JSON schema                           │
│   - run application unit tests                                  │
│   Duration: 1-3 minutes                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Smoke Eval (all AI changes)                            │
│   - run 20-50 core eval cases                                   │
│   - keyword + semantic scoring                                  │
│   - block if pass rate < 0.70                                   │
│   Duration: 2-5 minutes, low cost                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  Prompt / Model      │
                   │  change detected?    │
                   └──────────┬───────────┘
                         Yes  │  No → deploy to staging
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Full Eval (prompt / model changes only)                │
│   - run 200-400 cases                                           │
│   - composite scoring including LLM-as-judge                   │
│   - block if pass rate < 0.80                                   │
│   - generate diff report vs baseline                            │
│   Duration: 15-30 minutes, moderate cost                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       deploy to staging
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Staging Validation                                     │
│   - smoke integration test against staging environment          │
│   - canary behavioral check                                     │
│   Duration: 5-10 minutes                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       promote to production
```

## GitHub Actions Example

```yaml
name: AI Platform CI

on:
  pull_request:
    paths:
      - 'prompts/**'
      - 'applications/**'
      - 'projects/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python -m pytest tests/unit/ -q

  smoke-eval:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Run smoke evaluation
        run: |
          python scripts/eval/run_eval.py \
            --dataset eval/datasets/smoke-20cases.json \
            --prompt prompts/rag-grounding/$(cat prompts/registry.json | jq -r '."rag-grounding".dev') \
            --output eval/runs/smoke-${{ github.sha }}.json \
            --threshold 0.70
        env:
          MODEL_API_URL: ${{ secrets.STAGING_MODEL_API_URL }}
          MODEL_API_KEY: ${{ secrets.STAGING_MODEL_API_KEY }}

  full-eval:
    needs: smoke-eval
    if: contains(github.event.pull_request.changed_files, 'prompts/')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run full evaluation
        run: |
          python scripts/eval/run_eval.py \
            --dataset eval/datasets/rag-eval-v3.1.json \
            --prompt prompts/rag-grounding/$(cat prompts/registry.json | jq -r '."rag-grounding".dev') \
            --output eval/runs/full-${{ github.sha }}.json \
            --threshold 0.80 \
            --diff-against eval/baselines/current.json
```

## Evaluation Artifacts

Every CI eval run should produce and archive:

- the full per-case scores
- the aggregate report (pass rate, mean score, category breakdown)
- the diff report against baseline
- the prompt version and model pin used
- the eval dataset version used

These artifacts are auditable records of the validation that allowed a change to reach production.

## Deployment Strategies

### Canary Deployment For Prompt Changes

Route a small percentage of traffic to the new prompt version before full rollout:

```
10% traffic → prompt v1.5.0 (new)
90% traffic → prompt v1.4.0 (stable)
```

Monitor quality signals on both cohorts for 24-48 hours before promoting the new version to 100%.

### Blue/Green For Model Version Changes

When switching model versions, maintain two identical environments and flip traffic at the gateway level:

- Blue: current model version, serving 100% traffic
- Green: new model version, tested and ready
- Switch: gateway routing change (instant, instant rollback possible)

## Cost Management In CI

Evaluation costs should be tracked as a project expense:

- log model API cost per eval run to a cost tracking system
- set a per-PR eval budget (e.g., $0.50 maximum for smoke eval)
- run expensive full eval only on relevant changes, not on every PR
- cache model responses for identical inputs to avoid re-running the same eval cases repeatedly

Most teams spend $50-200/month on CI evaluation at a reasonable scale. Track it from the start before it grows unnoticed.
