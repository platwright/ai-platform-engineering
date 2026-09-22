# GitOps Repository Structure

This document describes the recommended GitOps repository layout for the Acme AI platform.

## Repository Separation Pattern

The platform uses two repositories:

| Repository | Purpose |
|---|---|
| `ai-platform-engineering` (this repo) | Course content, application code, Kubernetes manifests |
| `ai-platform-config` (separate, not in this course) | Environment-specific values and secrets references |

Separating config from code avoids leaking environment differences into the application source tree and enables promotion without code changes.

## Manifest Layout In This Repository

```text
platform/kubernetes/
├── ai-gateway/
│   ├── base/               ← platform-team-owned manifests
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── dev/            ← dev-specific patches (fewer replicas, cheaper images)
│       └── prod/           ← prod patches (replicas, resource limits, HPA)
├── rag-platform/
│   └── ... (same pattern)
├── model-serving-vllm/
│   └── ... (same pattern)
└── gpu-workloads/
    └── ... (same pattern)
```

## Kustomize Overlay Pattern

Each service follows the same base + overlay pattern:

```bash
# Render dev overlay
kubectl kustomize platform/kubernetes/ai-gateway/overlays/dev

# Render prod overlay (requires kubectl 1.21+)
kubectl kustomize platform/kubernetes/ai-gateway/overlays/prod

# Apply to cluster
kubectl apply -k platform/kubernetes/ai-gateway/overlays/dev
```

## ArgoCD Application Mapping

Each Kubernetes directory maps to one ArgoCD Application object. See [argo-application.yaml](argo-application.yaml) for the Application manifests.

```text
ArgoCD Application        →  Kubernetes Path
─────────────────────────────────────────────────────────────────
ai-gateway-stack          →  platform/kubernetes/ai-gateway
rag-platform-stack        →  platform/kubernetes/rag-platform
model-serving-stack       →  platform/kubernetes/model-serving-vllm
```

## Promotion Flow

See [promotion-workflow.md](promotion-workflow.md) for the full environment promotion procedure.

## Secrets Management

Manifests in this repository never contain real secrets. Environment-specific secrets are managed outside this repository using one of:

- **Kubernetes Secrets** populated by an external-secrets operator from a vault
- **Sealed Secrets** (Bitnami) committed as encrypted objects
- **Helm chart values** injected at deploy time from a secrets manager

The placeholder pattern used in `config/app.example.json` throughout this course reflects the same principle: templates show structure, not values.
