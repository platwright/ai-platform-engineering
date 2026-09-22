# Module 07 Lab

## Goal

Run Project 02 in mock mode, render the vLLM serving manifests, and understand the serving metrics they are designed to support.

## Outcome

By the end of this lab, you should have:

- generated a benchmark report for an OpenAI-compatible endpoint in mock mode
- rendered the vLLM manifest set locally
- identified the serving metrics that matter most for chat-style inference

## Step 1 - Run The Mock Benchmark

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

## Step 2 - Review The Report

Inspect:

- success rate
- p50, p95, and p99 latency
- completion tokens per second
- failure count

## Step 3 - Render The vLLM Manifests

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

## Step 4 - Optional Live Endpoint Path

If you have a live OpenAI-compatible endpoint, benchmark it:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode http --endpoint http://127.0.0.1:8001/v1/chat/completions --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## Step 5 - Reflection

Write down:

- which metric best reflects user experience
- which metric best reflects hardware efficiency
- which serving choices would change first if p95 latency was too high