# Module 15 Concepts

## Latency Is A Waterfall, Not A Single Number

Every AI request moves through multiple sequential stages. Each stage adds to total latency. Reporting a single end-to-end number hides which stage is the bottleneck. The first step in any performance investigation is decomposing the waterfall.

## GPU Memory Bounds Concurrency, Not Just Speed

For model serving, the relevant constraint is often GPU memory, not GPU compute. KV cache consumes memory proportional to sequence length and batch size. When memory fills, requests queue. Adding compute does not help a memory-bound serving workload; only adding memory (larger GPU) or reducing context length does.

## TTFT And Throughput Trade Off Against Each Other

Serving optimizations that increase throughput (larger batches, longer sequences, more efficient KV cache use) often increase TTFT because the model must wait for a full batch before processing begins. Optimizations that minimize TTFT (smaller batches, eager processing) reduce throughput. Setting the right operating point requires knowing which SLO is more important for your use case.

## CPU Autoscaling Is Wrong For Model Serving

Model serving pods are not CPU-bound. A model serving pod can have 5% CPU utilization and be completely saturated on GPU memory with a full request queue. Autoscaling based on CPU produces no scaling when needed and potentially over-scales on proxy workloads that have high CPU for other reasons.

## Real Load Tests Use Real Prompts

A load test that sends 5-token prompts and measures requests per second tells you nothing about production performance at typical context lengths. AI load tests must use prompt distributions that reflect actual production input length distributions.

## Quantization Is A Quality-Cost Tradeoff

Quantizing a model from FP16 to INT4 reduces memory by 4× and typically doubles throughput. It also degrades output quality in ways that vary by model and task. Never deploy quantized models without running your evaluation suite to measure the quality impact on your specific workload.
