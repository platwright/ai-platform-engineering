# Project 02 Lab

## Goal

Validate the benchmark locally, render the vLLM manifests, and prepare a repeatable path for benchmarking an open model endpoint.

## Step 1 - Run The Mock Benchmark

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

This should generate JSON and Markdown reports under `projects/project-02-ai-gateway/runs/`.

## Step 2 - Review The Metrics

Inspect:

- total requests
- successful versus failed requests
- p50, p95, and p99 latency
- estimated completion tokens per second

## Step 3 - Render The Kubernetes Manifests

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

## Step 4 - Optional Cluster Path

If you have a GPU-capable cluster and the required image/model access, adapt the manifest set and deploy it.

Then benchmark through a port-forward or exposed service:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode http --endpoint http://127.0.0.1:8001/v1/chat/completions --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## Step 5 - Reflection

Write down:

- which metrics you would trust for a first performance review
- which metrics are missing without deeper server-side observability
- which serving assumptions would change between development and production