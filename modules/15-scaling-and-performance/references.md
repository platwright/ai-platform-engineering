# Module 15 References

## Inference Performance

- [vLLM Documentation](https://docs.vllm.ai/) — comprehensive guide to vLLM serving options, continuous batching, chunked prefill
- [PagedAttention Paper](https://arxiv.org/abs/2309.06180) — the foundation of vLLM's KV cache management
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](https://www.usenix.org/conference/osdi22/presentation/yu) — the continuous batching paper

## Quantization

- [AWQ: Activation-aware Weight Quantization](https://arxiv.org/abs/2306.00978) — efficient INT4 quantization with minimal quality loss
- [GPTQ: Accurate Post-Training Quantization](https://arxiv.org/abs/2210.17323) — quantization approach for LLM deployment
- [llama.cpp GGUF quantization formats](https://github.com/ggerganov/llama.cpp#quantization) — practical quantization format guide

## Scaling and Autoscaling

- [KEDA Documentation](https://keda.sh/docs/) — event-driven autoscaling for Kubernetes
- [Kubernetes HPA Documentation](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) — native autoscaling reference
- [Optimizing LLM Inference (Anyscale)](https://www.anyscale.com/blog/llm-inference-performance-engineering-best-practices) — practical inference optimization guide

## GPU and Hardware

- [NVIDIA H100 Architecture](https://resources.nvidia.com/en-us-tensor-core/nvidia-tensor-core-gpu-datasheet) — hardware capabilities
- [NVIDIA GPU Comparison](https://www.nvidia.com/en-us/data-center/resources/compare-models/) — data center GPU specifications
- [Artificial Analysis GPU Rankings](https://artificialanalysis.ai/) — independent benchmarks across models and hardware

## Load Testing

- [Locust](https://locust.io/) — Python-based load testing framework
- [k6](https://k6.io/) — developer-friendly load testing for APIs
- [LLMPerf](https://github.com/ray-project/llmperf) — LLM-specific performance benchmarking

## Architecture

- [Inference at Scale (Modal)](https://modal.com/blog/llm-serving-guide) — practical guide to LLM serving at scale
- [Serving Llama at Scale (Anyscale)](https://www.anyscale.com/blog/how-anyscale-scales-llms) — production serving architecture patterns
