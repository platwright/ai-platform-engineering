# Module 15 - Scaling and Performance

## Overview

Scaling AI systems is not the same as scaling web applications. Inference is stateful at the hardware level (KV cache), throughput is bounded by GPU memory as much as compute, and token generation rate is a fundamentally different metric than requests per second.

This module decomposes AI platform latency end to end and teaches workload-aware scaling strategies across the application tier, AI gateway, and model serving layers. It bridges the infrastructure understanding from Modules 05 and 06 with the practical performance engineering work that comes from real production traffic.

## Learning Objectives

By the end of this module, you should be able to:

- decompose end-to-end latency for an AI workload into its constituent parts
- apply horizontal and vertical scaling strategies to the application, gateway, and serving layers
- design autoscaling policies that use inference-specific metrics rather than CPU
- explain how batching, KV cache eviction, and quantization affect throughput under load
- conduct an AI-aware load test that measures the right signals
- identify and reason about common performance bottlenecks in AI serving stacks
- make informed decisions between scale-up and scale-out for inference workloads

## Prerequisites

- Completion of [modules/14-reliability/README.md](../14-reliability/README.md)
- Completion of [modules/07-model-serving/README.md](../07-model-serving/README.md) and [modules/06-gpu-and-accelerators/README.md](../06-gpu-and-accelerators/README.md)
- Completion of Project 02

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [End-to-End Latency Decomposition](chapters/01-end-to-end-latency-decomposition.md)
2. [Scaling the Application Tier](chapters/02-scaling-the-application-tier.md)
3. [Scaling the AI Gateway](chapters/03-scaling-the-ai-gateway.md)
4. [Scaling Model Serving](chapters/04-scaling-model-serving.md)
5. [Scale-Up vs Scale-Out for Inference](chapters/05-scale-up-vs-scale-out.md)
6. [Autoscaling with Inference-Specific Metrics](chapters/06-autoscaling-with-inference-metrics.md)
7. [AI-Aware Load Testing](chapters/07-ai-aware-load-testing.md)
8. [Inference Scheduling and Batching](chapters/08-inference-scheduling-and-batching.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Expected Outcome

At the end of this module, you should have:

- a clear latency decomposition for the sample-rag request path
- a completed benchmark run from Project 02 with analysis
- notes on which scaling lever addresses each bottleneck type
- a designed autoscaling policy for the model serving deployment

## Knowledge Check

1. List the components of end-to-end AI request latency in order. Which is typically the largest contributor?
2. Why does TTFT degrade under high concurrency even when GPU utilization appears acceptable?
3. What is the difference between tensor parallelism and pipeline parallelism? When do you need each?
4. Why is CPU-based HPA unsuitable for autoscaling model serving pods?
5. What does an AI load test measure that a standard HTTP load test (e.g., `ab` or `wrk`) misses?
6. How does continuous batching differ from dynamic batching, and why does it matter for TTFT?
7. When should you choose scale-up (larger GPU) over scale-out (more replicas)?

## Common Mistakes

- using CPU utilization as the autoscaling metric for model serving
- load testing with artificially short prompts that do not reflect real token distributions
- measuring only average latency and missing p95/p99 behavior under load
- confusing GPU utilization with GPU memory utilization (both matter but in different ways)
- scaling the application tier without realizing the bottleneck is in model serving
- adding more replicas without verifying that the load balancer distributes requests correctly

## Production Considerations

- set max_tokens limits before load testing — unbounded generation produces misleading throughput numbers
- batch size and parallelism choices made during deployment are hard to change without service restart
- autoscaling is not a substitute for capacity planning — know your peak load before it arrives
- quantization tradeoffs affect quality as well as throughput — benchmark with your actual eval dataset
- TTFT SLOs should inform your target concurrency range, not the other way around

## Next Step

Read [concepts.md](concepts.md), then run the Project 02 benchmark in [lab.md](lab.md).

## Overview

Scaling AI systems is not the same as scaling web applications. Inference is stateful at the hardware level (KV cache), throughput is bounded by GPU memory as much as compute, and token generation rate is a fundamentally different metric than requests per second.

This module decomposes AI platform latency from end to end and teaches workload-aware scaling strategies across the application tier, AI gateway, and model serving layers. It bridges the infrastructure-level understanding from Module 05 and Module 06 with the practical performance engineering work that comes from real production traffic.

## Intended Learning Objectives

By the end of this module, learners should be able to:

- decompose end-to-end latency for an AI workload into its components
- apply horizontal and vertical scaling strategies to the application, gateway, and serving layers
- design autoscaling policies that account for inference-specific metrics
- explain how batching, KV cache eviction, and quantization affect throughput under load
- use AI-aware load testing to measure serving capacity
- identify and resolve common performance bottlenecks in AI serving stacks

## Prerequisites

- Completion of Module 14 (Reliability)
- Completion of Module 07 (Model Serving) and Module 06 (GPU and Accelerators)
- Completion of Project 02

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Planned Chapter Structure

1. End-to-End Latency Decomposition
2. Scaling the Application Tier
3. Scaling the AI Gateway
4. Scaling Model Serving
5. Scale-Up vs Scale-Out for Inference
6. Autoscaling with Inference-Specific Metrics
7. AI-Aware Load Testing
8. Inference Scheduling and Batching

## Planned Module Assets

- concepts.md
- architecture.md: latency decomposition diagram and scaling topology
- lab.md: run the Project 02 benchmark against a local serving stack, identify the bottleneck, and apply a mitigation
- challenge.md
- verification.md
- solution.md
- references.md

## Planned Lab Scope

The lab will:

1. Run the Project 02 benchmark against the local vLLM stack at low and high concurrency
2. Measure TTFT, tokens/second, and queue depth at different load levels
3. Identify where the bottleneck is: application, gateway, or model serving
4. Apply a targeted mitigation (e.g., batching, replicas, quantization) and re-measure

## Latency Decomposition

```
Total user-perceived latency = 
    network_client_to_gateway
  + gateway_processing
  + gateway_to_model_network
  + model_queue_wait
  + prefill_time          (processing input tokens)
  + time_to_first_token
  + generation_time       (output_tokens / tokens_per_second)
  + model_to_gateway_network
  + gateway_response_processing
  + network_gateway_to_client
```

Each component has a different scaling lever. Conflating them leads to incorrect root cause analysis and wasted optimization effort.

## Inference-Specific Scaling Metrics

| Metric | Scaling Implication |
|---|---|
| GPU memory utilization | KV cache eviction starts affecting latency at ~80% |
| Queue depth | Indicates under-provisioned serving capacity |
| Batch efficiency | Sparse batches waste GPU FLOPS |
| TTFT p95 | Sensitive to prefill time under high context load |
| Tokens per second | Bounded by GPU compute and memory bandwidth |
| KV cache hit rate | High hit rate reduces prefill cost for repeated prefixes |

## Production Considerations This Module Will Address

- Why does TTFT degrade under high concurrency even when GPU utilization looks acceptable?
- How do you autoscale a model serving deployment when the meaningful signal is queue depth, not CPU?
- What does an AI load test need to measure that a standard HTTP load test misses?
- How do you decide between adding GPU replicas versus upgrading GPU memory?

## Next Step

This module will be written in Phase 5. See [modules/16-ai-finops/README.md](../16-ai-finops/README.md) for the companion module.