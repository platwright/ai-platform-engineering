# GitOps Assets

This area holds GitOps-oriented deployment patterns and repository structure guidance for managing the AI platform declaratively.

## Available Assets

| File | Purpose |
|---|---|
| `argo-application.yaml` | ArgoCD Application and AppProject manifests for the AI gateway and RAG platform stacks |
| `repo-structure.md` | Recommended GitOps repository layout with Kustomize overlay pattern |
| `promotion-workflow.md` | Environment promotion flow from dev through staging to production |

## Relationship To Modules

GitOps patterns are introduced in Module 17 (Developer Platform) as part of the self-service and golden path discussion. Module 11 (LLMOps) references GitOps for prompt and config version management.

## Key Concepts

- Manifests in `platform/kubernetes/` use a `base/` + `overlays/` Kustomize pattern
- ArgoCD Applications point at overlay directories and sync automatically on merge to `main`
- Secrets are never committed — config templates use placeholder values only
- Promotion between environments is a pull request that updates the image tag in an overlay

See [repo-structure.md](repo-structure.md) for the full layout and [promotion-workflow.md](promotion-workflow.md) for the step-by-step promotion procedure.

