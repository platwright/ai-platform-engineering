# AI Gateway Kubernetes Stack

This manifest set provides a simple Kubernetes deployment shape for the local AI gateway service plus the Project 01 model API.

## Included Resources

- `namespace.yaml`
- `configmap-ai-gateway.yaml`
- `deployment-model-api.yaml`
- `service-model-api.yaml`
- `deployment-ai-gateway.yaml`
- `service-ai-gateway.yaml`
- `ingress-ai-gateway.yaml`
- `kustomization.yaml`

## Usage

Render the manifests:

```bash
kubectl kustomize platform/kubernetes/ai-gateway
```