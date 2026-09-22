# Advanced Labs

Deeper labs for GPU workloads, distributed inference, scaling behavior, multi-tenant platform operations, and production-readiness assessments.

## Available Labs

Labs in this area will be added alongside Modules 06, 07, 15, and 17.

### Planned

- **gpu-memory-pressure**: load a quantized model and progressively increase batch sizes, measuring throughput and latency until KV cache pressure causes degradation — covers Module 06
- **vllm-benchmark-analysis**: run the Project 02 benchmark at three concurrency levels and produce a comparative report identifying the throughput ceiling — covers Module 07
- **multi-tenant-rag-isolation**: create two RAG service tenants, attempt a cross-tenant query, and verify that the isolation boundary holds — covers Module 09
- **autoscaling-inference**: configure a Kubernetes HPA for the model serving deployment using custom queue-depth metrics and generate load to trigger scale-out — covers Modules 05 and 15
- **cost-attribution-report**: aggregate token usage logs from the AI gateway and produce a per-tenant cost report — covers Module 16
- **distributed-tracing-end-to-end**: instrument the full request path from the sample-chat application through the gateway to the model server and generate a Jaeger trace — covers Module 12

## Prerequisites For Advanced Labs

- A local Kubernetes cluster with GPU node access (for GPU-specific labs) or CPU-only alternatives
- Project 01 through Project 04 completed
- The AI gateway and model serving stacks running
- Modules 06–10 complete or equivalent background knowledge

## Format

Each advanced lab has its own subdirectory with a detailed README, automation scripts, expected outputs, and a discussion section covering production implications.
