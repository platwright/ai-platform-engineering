# Module 07 - Model Serving

## Overview

This module turns model serving into a production engineering topic rather than a model demo. It explains what a model-serving system is, why inference performance behaves differently from ordinary APIs, and how serving choices affect latency, throughput, scalability, and platform design.

The module uses Project 02 as its executable companion and introduces a vLLM-based serving path on Kubernetes.

## Learning Objectives

By the end of this module, you should be able to:

- distinguish model, model server, inference API, routing layer, and application concerns
- explain why vLLM is relevant as a practical serving implementation
- describe the performance metrics that matter for inference systems
- explain batching, KV cache, quantization, and parallelism at a platform level
- compare Kubernetes-native serving options at a high level
- produce a basic performance report for a model-serving endpoint

## Prerequisites

- Completion of [modules/06-gpu-and-accelerators/README.md](../06-gpu-and-accelerators/README.md)
- Familiarity with the Kubernetes and container modules

GPU access is helpful for the full deployment path but not required for the benchmark and manifest-rendering path.

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [What Is Model Serving?](chapters/01-what-is-model-serving.md)
2. [Introduction to vLLM](chapters/02-introduction-to-vllm.md)
3. [Serving an Open Model](chapters/03-serving-an-open-model.md)
4. [Understanding Throughput and Latency](chapters/04-understanding-throughput-and-latency.md)
5. [Batching](chapters/05-batching.md)
6. [KV Cache](chapters/06-kv-cache.md)
7. [Quantization](chapters/07-quantization.md)
8. [Parallelism](chapters/08-parallelism.md)
9. [Kubernetes-Native Model Serving](chapters/09-kubernetes-native-model-serving.md)
10. [Distributed Inference](chapters/10-distributed-inference.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [projects/project-02-ai-gateway/README.md](../../projects/project-02-ai-gateway/README.md)
- [platform/kubernetes/model-serving-vllm/README.md](../../platform/kubernetes/model-serving-vllm/README.md)

## Expected Outcome

At the end of this module, you should have:

- a clear serving-focused mental model for inference systems
- one rendered vLLM manifest set
- a benchmark report from Project 02 mock mode or a live endpoint if available
- notes on how batching, KV cache, and quantization change serving capacity

## Knowledge Check

1. What is the difference between a model and a model server?
2. Why do TTFT and output-token speed matter separately?
3. How does batching increase throughput while affecting latency tradeoffs?
4. Why is KV cache a foundational serving resource?
5. What does quantization change operationally?
6. Why is distributed inference a different architectural step from single-node serving?

## Common Mistakes

- treating inference as an ordinary REST endpoint with no workload-specific metrics
- ignoring KV cache and context length when sizing serving infrastructure
- assuming one benchmark number explains all latency behavior
- confusing application routing concerns with model-serving concerns
- deploying a serving stack without a basic performance validation loop

## Production Considerations

- performance metrics should be tied to concrete request shapes and prompt sizes
- serving choices affect cost, latency, hardware efficiency, and failure modes together
- Kubernetes-native serving layers add rollout and routing control but also more operational surface area
- benchmarking without context can mislead; input and output token sizes matter

## Next Step

Read [concepts.md](concepts.md), then work through [projects/project-02-ai-gateway/README.md](../../projects/project-02-ai-gateway/README.md) using [lab.md](lab.md).# Module 07 - Model Serving

Status: Planned

This module will focus on inference serving as a production system rather than only a model demo.

Planned topics:

- model serving fundamentals
- vLLM introduction
- serving open models
- throughput and latency metrics
- batching and KV cache
- quantization and parallelism
- Kubernetes-native serving approaches