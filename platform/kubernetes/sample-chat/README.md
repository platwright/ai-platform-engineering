# Sample Chat Kubernetes Stack

This manifest set moves the sample chat stack from Docker Compose into Kubernetes.

## Included Resources

- `namespace.yaml`
- `configmap-sample-chat.yaml`
- `secret-openai-compatible-provider.template.yaml`
- `deployment-model-api.yaml`
- `service-model-api.yaml`
- `deployment-sample-chat.yaml`
- `service-sample-chat.yaml`
- `sample-chat-hpa.yaml`
- `batch-summary-job.yaml`
- `qdrant-service.yaml`
- `qdrant-statefulset.yaml`
- `ingress-sample-chat.yaml`
- `kustomization.yaml`

## Purpose

The resources are intentionally simple, but they cover the main Kubernetes objects Module 05 needs to teach:

- Deployment
- Job
- StatefulSet
- Service
- Ingress
- ConfigMap
- Secret
- PVC via StatefulSet volume claim templates
- HPA

## Usage

Render the manifests:

```bash
kubectl kustomize platform/kubernetes/sample-chat
```

Validate locally:

```bash
kubectl apply --dry-run=client -k platform/kubernetes/sample-chat
```

Apply to a cluster:

```bash
kubectl apply -k platform/kubernetes/sample-chat
```