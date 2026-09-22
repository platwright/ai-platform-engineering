# Module 06 - GPU And Accelerators

## Overview

This module explains why modern inference and training workloads often depend on accelerators and what that means for platform design. The goal is not to teach hardware engineering. The goal is to give platform engineers enough GPU and accelerator literacy to reason about model placement, memory limits, scheduling, sharing, capacity planning, and observability.

This is the first module where infrastructure cost and serving performance start to converge in a visible way.

## Learning Objectives

By the end of this module, you should be able to:

- explain why CPUs and GPUs behave differently for AI workloads
- describe the main GPU concepts a platform engineer needs to know
- estimate how model weights and KV cache consume accelerator memory
- explain the Kubernetes patterns used for GPU scheduling
- compare GPU sharing strategies such as time slicing and MIG
- design dedicated GPU node pools for different environments
- identify the core telemetry needed for GPU-backed AI platforms

## Prerequisites

- Completion of [modules/05-kubernetes-for-ai/README.md](../05-kubernetes-for-ai/README.md)
- Familiarity with the model-serving problem from the earlier modules

GPU hardware is useful but not required for the learning path in this module.

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 5 to 7 hours

## Module Map

### Chapters

1. [Why AI Uses GPUs](chapters/01-why-ai-uses-gpus.md)
2. [GPU Architecture for Platform Engineers](chapters/02-gpu-architecture-for-platform-engineers.md)
3. [GPU Memory](chapters/03-gpu-memory.md)
4. [GPU Scheduling in Kubernetes](chapters/04-gpu-scheduling-in-kubernetes.md)
5. [GPU Sharing](chapters/05-gpu-sharing.md)
6. [GPU Node Pools](chapters/06-gpu-node-pools.md)
7. [GPU Observability](chapters/07-gpu-observability.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [tools/gpu_memory_estimator.py](tools/gpu_memory_estimator.py)
- [platform/kubernetes/gpu-workloads/README.md](../../platform/kubernetes/gpu-workloads/README.md)

## Expected Outcome

At the end of this module, you should have:

- a practical mental model for accelerator-backed inference
- one or more sizing estimates from the GPU memory estimator
- a rendered set of GPU-oriented Kubernetes workload examples
- notes on how development, staging, and production GPU footprints differ

## Knowledge Check

1. Why do LLM workloads often prefer GPUs over CPUs?
2. Why is GPU memory often the first hard constraint during inference?
3. How do precision and quantization change deployment options?
4. Why is scheduling a GPU workload different from scheduling a CPU-only service?
5. When would time slicing or MIG be attractive, and what risks do they introduce?
6. Why should GPU node pools differ across environments?
7. Which GPU metrics matter most before users notice degradation?

## Common Mistakes

- thinking only about GPU count and ignoring GPU memory
- assuming all GPU types are interchangeable
- sizing by parameter count alone and ignoring KV cache growth
- treating accelerators as generic cluster resources with no placement policy
- forgetting that shared GPUs change isolation and performance assumptions

## Production Considerations

- accelerator cost and capacity planning should start before production traffic arrives
- GPU scheduling policies affect both utilization and reliability
- shared GPU strategies can improve efficiency while complicating observability and fairness
- GPU metrics need to be correlated with application metrics, not viewed in isolation

## Next Step

Read [concepts.md](concepts.md), use [tools/gpu_memory_estimator.py](tools/gpu_memory_estimator.py) through [lab.md](lab.md), and render the GPU workload examples in [platform/kubernetes/gpu-workloads/README.md](../../platform/kubernetes/gpu-workloads/README.md).# Module 06 - GPU And Accelerators

Status: Planned

This module will explain why AI workloads use accelerators and how platform teams manage them.

Planned topics:

- CPU versus GPU tradeoffs
- GPU architecture basics
- GPU memory and KV cache pressure
- Kubernetes GPU scheduling
- GPU sharing models
- node pool design and GPU observability