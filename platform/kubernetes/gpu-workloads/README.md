# GPU Workload Examples

This manifest set provides simple GPU-oriented Kubernetes workloads for Module 06.

## Included Resources

- `namespace.yaml`
- `pod-gpu-smoke-check.yaml`
- `deployment-gpu-inference.yaml`
- `service-gpu-inference.yaml`
- `job-gpu-batch-embeddings.yaml`
- `kustomization.yaml`

## Usage

Render the manifests:

```bash
kubectl kustomize platform/kubernetes/gpu-workloads
```

These examples are primarily for inspection and discussion. They are intentionally small and cluster-agnostic aside from their GPU resource requests.