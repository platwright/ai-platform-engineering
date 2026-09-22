# Module 07 Verification

## Required Checks

Run the mock benchmark:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

Expected result:

- benchmark summary prints successfully
- JSON and Markdown reports are created

Render the serving manifests:

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

Expected result:

- namespace, deployment, service, and ingress render successfully

## Understanding Check

You should be able to explain:

- the difference between the model and the serving runtime
- why TTFT and tokens/sec are distinct metrics
- how batching and KV cache affect efficiency
- why quantization and parallelism exist in serving systems
- what Project 02 proves and what it still leaves unanswered