# Project 02 Verification

## Required Checks

Run the mock benchmark:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

Expected result:

- exit code `0`
- a JSON report and a Markdown report under `runs/`
- summary output including request counts and latency percentiles

Render the Kubernetes manifests:

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

Expected result:

- the namespace, deployment, service, and ingress render successfully

Optional compile check:

```bash
python -m py_compile projects/project-02-ai-gateway/benchmark_openai_compatible.py
```