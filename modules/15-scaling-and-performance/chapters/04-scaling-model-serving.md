# Chapter 04 - Scaling Model Serving

## Model Serving Is The Hard Scaling Layer

Every other layer in the AI stack scales horizontally with commodity compute. Model serving requires expensive GPU hardware, which changes the scaling economics and the operational approach.

The primary constraints are:
1. **GPU VRAM**: model weights + KV cache must fit in memory
2. **GPU compute (FLOPS)**: prefill and generation throughput
3. **Memory bandwidth**: how fast weights can be loaded during generation

Understanding which constraint is active determines which scaling strategy applies.

## Scaling With Replicas (Scale-Out)

Adding model serving replicas is the simplest scaling lever: more GPUs, more concurrency.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-serving
spec:
  replicas: 3  # 3 GPU pods
```

Scale-out works well when:
- requests are independent (no cross-request state in the serving layer)
- the model fits in a single GPU's VRAM
- you have multiple identical GPUs available

Scale-out does NOT help when:
- the model is too large for a single GPU (needs tensor parallelism)
- the bottleneck is prefill latency for very long inputs (more replicas don't reduce per-request prefill time)
- GPU memory is the constraint and you need more memory per request, not more requests

## Tensor Parallelism (Scale-Up Across GPUs)

Tensor parallelism splits model layers across multiple GPUs. The computation for each forward pass is distributed:

```
Single GPU (70B model, ~140GB VRAM needed):
  → Does NOT fit on one A100 (80GB VRAM)

2× A100 with tensor parallelism:
  → Each GPU holds half the weights
  → Synchronization via NVLink on every layer
  → Higher throughput, lower latency
  → Requires NVLink or fast interconnect

vLLM tensor parallel serving:
  vllm serve model --tensor-parallel-size 2 --gpu-memory-utilization 0.9
```

Tensor parallelism is typically used when the model is too large for a single GPU or when you need very high throughput from a single model instance.

## Pipeline Parallelism

Pipeline parallelism splits the model vertically by layers across GPUs:

- GPU 1: layers 1–16
- GPU 2: layers 17–32

Requests flow through the pipeline. This introduces pipeline bubble latency but allows serving very large models across commodity GPUs without NVLink.

Use pipeline parallelism when tensor parallelism is not feasible due to interconnect limitations.

## Data Parallelism

Data parallelism runs independent full model copies. Each replica handles different requests. This is effectively scale-out with each replica potentially spanning multiple GPUs via tensor parallelism.

## KV Cache Optimization

The KV cache is the primary memory consumer during serving. Strategies to reduce its footprint:

| Strategy | Memory Reduction | Quality Impact |
|---|---|---|
| Quantized KV cache (INT8) | ~2× | Minimal for most models |
| Quantized KV cache (INT4) | ~4× | Noticeable on long contexts |
| Prefix caching | Reduces duplicated prefixes | None (reuse, not compression) |
| vLLM PagedAttention | Better memory efficiency | None (management improvement) |

## Quantization

Running a quantized model reduces VRAM requirements and increases throughput:

| Precision | VRAM Reduction | Throughput Gain | Quality Impact |
|---|---|---|---|
| FP16 (baseline) | 1× | 1× | None |
| INT8 (AWQ, GPTQ) | ~2× | 1.5–2× | Minor |
| INT4 (GGUF Q4_K_M) | ~4× | 2–3× | Moderate |

Always evaluate quality impact on your specific workload before deploying a quantized model.

## Serving Configuration for vLLM

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct \
  --tensor-parallel-size 1 \
  --max-num-seqs 256 \          # max concurrent sequences (queue + active)
  --gpu-memory-utilization 0.9 \ # leave 10% headroom
  --max-model-len 32768 \        # max context length
  --enable-prefix-caching        # reuse KV cache for repeated prefixes
```

Monitor `vllm_gpu_cache_usage_perc` to determine if memory utilization needs adjustment.
