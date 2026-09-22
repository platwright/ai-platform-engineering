# Chapter 03 - GPU Utilization and Self-Hosted Cost

## The Effective Cost Formula

Self-hosted GPU serving has a fixed infrastructure cost regardless of actual inference volume. Effective cost per inference depends entirely on utilization:

```
effective_cost_per_inference_hour =
    gpu_instance_cost_per_hour / gpu_utilization_fraction

Examples:
  A10G at $1.50/hr, 20% utilization → $7.50/effective hour
  A10G at $1.50/hr, 50% utilization → $3.00/effective hour
  A10G at $1.50/hr, 80% utilization → $1.88/effective hour
  A10G at $1.50/hr, 95% utilization → $1.58/effective hour
```

A GPU sitting mostly idle is not cheap. It is the most expensive possible serving configuration.

## Measuring GPU Utilization

The NVIDIA DCGM exporter exposes GPU utilization as a Prometheus metric:

```promql
# GPU compute utilization (percentage)
DCGM_FI_DEV_GPU_UTIL

# GPU memory utilization (percentage)
DCGM_FI_DEV_MEM_COPY_UTIL

# Alternatively from vLLM:
vllm_gpu_cache_usage_perc  # KV cache memory as proxy for serving utilization
```

For FinOps purposes, track:
- average utilization over 24-hour periods
- utilization distribution by hour of day (to identify low-utilization windows)
- minimum utilization (idle waste)

## Common Waste Patterns

### Over-Provisioned Dev/Staging

Dev and staging environments often run GPU instances 24/7 but use them for a few hours of testing per day. This is typically 90%+ waste.

Fix: scheduled shutdown during off-hours, or switch dev/staging to CPU-based serving.

### Idle Production Replicas

Autoscaling adds replicas during peaks but may not scale down aggressively due to cooldown periods or minimum replica settings.

Fix: tune autoscaling scale-down aggressiveness, measure idle time per replica.

### Batch Job On Interactive GPU

Running a batch job (nightly embedding reindex, eval runs) on the same GPU as interactive serving.

Fix: separate GPU pools for batch vs interactive, or schedule batch jobs during off-peak hours when interactive GPUs would otherwise be idle.

### Model Too Large For Workload

Deploying a 70B model when an 8B model would serve the workload at the required quality. The 70B model needs more GPUs and produces higher cost per inference.

Fix: evaluate quality tradeoff of smaller models against cost difference.

## Cost Per Thousand Tokens (Self-Hosted)

Convert GPU cost to a per-token equivalent for comparison with hosted APIs:

```python
def cost_per_million_tokens(
    gpu_hourly_rate: float,
    tokens_per_second: float,
    utilization: float = 0.70
) -> float:
    """
    gpu_hourly_rate: $ per hour of the GPU instance
    tokens_per_second: output token generation rate
    utilization: fraction of time the GPU is actually generating tokens
    """
    effective_rate = gpu_hourly_rate / utilization
    tokens_per_hour = tokens_per_second * 3600 * utilization
    return effective_rate / (tokens_per_hour / 1_000_000)

# A10G at $1.50/hr, 40 tok/s, 70% utilization:
cost = cost_per_million_tokens(1.50, 40, 0.70)
# → ~$0.015 per million tokens

# Compare to hosted GPT-4o mini output: $0.60 per million tokens
# Self-hosting is 40× cheaper if utilization is maintained
```

Self-hosted open-weight models are dramatically cheaper per token at volume, but that cost advantage only holds at high utilization. Low utilization eliminates the advantage.

## GPU Instance Pricing Options

| Option | Cost | Notes |
|---|---|---|
| On-demand | Full price | Flexible, expensive for sustained use |
| Reserved (1-year) | ~40% discount | Requires commitment, best for production baselines |
| Reserved (3-year) | ~60% discount | Best for stable, long-running workloads |
| Spot/preemptible | ~70% discount | Can be interrupted; suitable for batch only |

For production interactive serving, use reserved instances for the baseline capacity and on-demand for burst. For batch workloads (eval, reindex, batch summarization), use spot instances.
