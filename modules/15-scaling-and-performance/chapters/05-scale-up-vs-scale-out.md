# Chapter 05 - Scale-Up vs Scale-Out for Inference

## The Core Decision

When performance is insufficient, you have two options:

- **Scale-up**: use a larger, more powerful GPU (more VRAM, faster memory bandwidth)
- **Scale-out**: add more GPU replicas of the same kind

The right answer depends on which constraint is active.

## When Scale-Up Is The Answer

### Model Doesn't Fit on Single GPU

A 70B parameter FP16 model needs ~140GB VRAM. An A100 80GB cannot host it alone. Options:
- A single H100 NVL (94GB VRAM) cannot fit it either
- Two A100s with tensor parallelism: fits with headroom for KV cache
- Scale-up to a larger instance (8× A100 or H100 node)

### KV Cache Is The Bottleneck

When the GPU has compute to spare but KV cache fills up quickly, you need more memory per serving instance, not more instances.

Symptom: `vllm_gpu_cache_usage_perc` stays near 90–100% even at moderate concurrency.

Fix: use a GPU with more VRAM (A100 80GB over A10G 24GB), or use a quantized KV cache.

### Very Long Context Requests

Requests with 100K+ token contexts need large KV caches. A single such request may use as much GPU memory as 20 typical requests. Scale-up (more VRAM) handles these better than scale-out.

## When Scale-Out Is The Answer

### Throughput Is The Goal (Not Latency)

Scale-out increases total throughput by adding more concurrent serving capacity. If your platform needs to handle 1,000 requests per minute and one GPU handles 200/minute, you need 5 GPUs.

### Model Fits On One GPU

If your model (e.g., Llama 3.1 8B, ~16GB FP16) fits comfortably on one A10G (24GB), scaling out with more A10G instances is cheaper than upgrading to larger GPUs.

### Geographic Distribution

Serving different regions from geographically distributed replicas reduces network latency. This is a scale-out decision regardless of per-instance size.

### Cost Efficiency

A10G instances cost roughly 1/3 of an A100 instance. Three A10G instances may provide better throughput-per-dollar than one A100 for models that fit on a single A10G.

## The Decision Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│  Model too large for one GPU?         → Scale-up (tensor para)  │
│  KV cache fills under low concurrency?→ Scale-up (more VRAM)    │
│  Very long context requests?          → Scale-up                │
│  Need more total throughput?          → Scale-out               │
│  Model fits comfortably on one GPU?   → Scale-out               │
│  Cost-per-inference is too high?      → Scale-out (cheaper GPUs)│
│  Latency is acceptable, need volume?  → Scale-out               │
└─────────────────────────────────────────────────────────────────┘
```

## Mixed Strategies

Most production deployments use both:

- **Base capacity**: 2–4 replicas for HA and load distribution
- **Burst capacity**: scale-out with autoscaling to handle traffic spikes
- **Large model**: tensor parallelism within each replica to fit the model

Example: a 70B model deployment with 2 replicas, each using 2× A100s with tensor parallelism. Autoscaling adds more 2-GPU replica units when queue depth rises.

## GPU Selection Reference

| GPU | VRAM | Notes |
|---|---|---|
| NVIDIA T4 | 16GB | Cost-effective for 7–8B models at FP16 |
| NVIDIA A10G | 24GB | Good for 7–13B models; common in AWS |
| NVIDIA L4 | 24GB | More efficient successor to A10G |
| NVIDIA A100 40GB | 40GB | Older, less cost-effective now |
| NVIDIA A100 80GB | 80GB | Good for 30–70B models |
| NVIDIA H100 SXM | 80GB | Fastest current option; high cost |
| NVIDIA H200 | 141GB | Can fit most large models on one GPU |

Check current cloud pricing before committing; GPU availability and pricing change frequently.
