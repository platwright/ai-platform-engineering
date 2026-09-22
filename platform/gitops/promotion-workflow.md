# Environment Promotion Workflow

This document describes the promotion flow for AI platform services from development through staging to production.

## Environments

| Environment | Cluster | Namespace Suffix | Purpose |
|---|---|---|---|
| `dev` | local kind/k3d | `-dev` | Developer iteration and integration testing |
| `staging` | shared cloud cluster | `-staging` | Pre-production validation and load testing |
| `prod` | production cluster | (no suffix) | Live traffic |

## Promotion Steps

### 1. Merge To Main

All changes start as a pull request. The PR must pass:

- [ ] Python lint and unit tests (if applicable)
- [ ] Kubernetes manifest linting (`kubectl kustomize` renders without errors)
- [ ] Evaluation gate: eval pass rate ≥ 0.80 on `eval/datasets/rag-smoke.json`
- [ ] Security scan: no secrets in tracked files (`git grep` check)

### 2. Deploy To Dev

ArgoCD automatically syncs `main` to the `dev` environment within 2 minutes of merge. No manual step required.

Verify dev deployment:
```bash
kubectl get pods -n ai-gateway-dev
kubectl rollout status deployment/ai-gateway -n ai-gateway-dev
```

### 3. Smoke Test Dev

Run the smoke eval against the dev environment:
```bash
RAG_BASE_URL=http://rag-platform-dev:8090 \
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.80
```

### 4. Promote To Staging

Create a pull request that updates the staging overlay to the new image tag:

```bash
# In the platform-config repository (separate from this repo)
git checkout -b promote/ai-gateway-v1.2.3
# Edit overlays/staging/kustomization.yaml: update newTag
git push
# Create PR, get approval, merge
```

ArgoCD syncs staging automatically after merge.

### 5. Validate Staging

Run the full evaluation suite and load test:
```bash
python eval/run_eval.py \
  --dataset eval/datasets/rag-smoke.json \
  --service-name team-a-kb \
  --threshold 0.80

python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode http \
  --endpoint http://ai-gateway-staging/v1/chat/completions \
  --requests 100
```

Staging must pass for 30 minutes before proceeding.

### 6. Promote To Production

Create a second PR updating the `prod` overlay. Requires two approvals from the platform team.

### 7. Production Validation

After deployment:
- Monitor TTFT p95 for 15 minutes
- Check error rate in gateway metrics
- Verify eval score has not regressed

## Rollback Procedure

To roll back immediately:
```bash
# Revert to previous ArgoCD revision
argocd app rollback ai-gateway-stack <previous-revision-id>
```

Or update the prod overlay to the last known good image tag and merge.

## Promotion Checklist Template

Copy this checklist into your PR description for prod promotions:

```markdown
## Promotion Checklist

- [ ] CI passed on main (eval ≥ 0.80, no lint errors, no secrets)
- [ ] Dev deployed and stable for > 30 minutes
- [ ] Staging deployed and smoke test passed
- [ ] Load test shows no p95 regression vs baseline
- [ ] Two platform team approvals received
- [ ] Rollback procedure reviewed
```
