# Kubernetes Assets

This area holds manifests and examples used across the runtime modules.

## Available Assets

- [sample-chat/README.md](sample-chat/README.md): Kubernetes stack for the sample chat application and Project 01 model API
- [gpu-workloads/README.md](gpu-workloads/README.md): GPU scheduling examples for Module 06
- [model-serving-vllm/README.md](model-serving-vllm/README.md): vLLM serving stack for Module 07 and Project 02
- [ai-gateway/README.md](ai-gateway/README.md): Kubernetes stack for the AI gateway and Project 01 model API

## Typical Commands

Render the sample chat stack:

```bash
kubectl kustomize platform/kubernetes/sample-chat
```

Render the GPU examples:

```bash
kubectl kustomize platform/kubernetes/gpu-workloads
```

Render the vLLM stack:

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

Render the AI gateway stack:

```bash
kubectl kustomize platform/kubernetes/ai-gateway
```