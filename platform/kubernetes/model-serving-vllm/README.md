# vLLM Kubernetes Stack

This manifest set provides a minimal Kubernetes deployment shape for serving an open model through vLLM.

## Included Resources

- `namespace.yaml`
- `secret-huggingface.template.yaml`
- `deployment-vllm.yaml`
- `service-vllm.yaml`
- `ingress-vllm.yaml`
- `kustomization.yaml`

## Usage

Render the manifests:

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

If you have a compatible cluster, apply them after updating the model name, image, and secret values for your environment.