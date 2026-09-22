# Project 02 - Open Model Serving on Kubernetes

## Goal

Deploy an open model behind a vLLM-based OpenAI-compatible API surface, expose it through Kubernetes, and produce a basic performance report from load testing.

The directory path remains `project-02-ai-gateway` from the initial scaffold, but the project content follows the curriculum plan for Project 02 in the model-serving section.

## What You Will Build

- a benchmark tool for OpenAI-compatible inference endpoints
- a report generator for latency and throughput observations
- a Kubernetes manifest set for a vLLM deployment
- a repeatable path for port-forwarding or exposing the service and testing it

## Why This Project Matters

Project 01 taught application-side model abstraction. Project 02 moves one layer deeper into inference infrastructure.

This is where the course starts to separate:

- model artifact
- model server
- inference API
- Kubernetes runtime
- performance validation

## Project Files

- `benchmark_openai_compatible.py`: load generator and report writer
- `prompts/benchmark-prompts.txt`: default prompt set for the benchmark
- `fixtures/benchmark-mock-series.json`: mock responses for local validation
- `runs/`: generated JSON and Markdown reports

## Runtime Assets

- [platform/kubernetes/model-serving-vllm/README.md](../../platform/kubernetes/model-serving-vllm/README.md): Kubernetes manifest set for a vLLM deployment

## Documentation

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Quick Start

Validate the benchmark locally without a model server:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

Render the vLLM manifest set:

```bash
kubectl kustomize platform/kubernetes/model-serving-vllm
```

If you have a cluster and a reachable OpenAI-compatible endpoint, benchmark it:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode http --endpoint http://127.0.0.1:8001/v1/chat/completions --model TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## Relationship To Module 07

This project is the executable companion to the model serving module and gives the learner a basic load-testing and reporting workflow they can reuse later.