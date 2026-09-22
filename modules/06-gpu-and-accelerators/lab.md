# Module 06 Lab

## Goal

Estimate GPU memory requirements for a model-serving workload and render GPU-oriented Kubernetes workload examples.

## Outcome

By the end of this lab, you should have:

- run the GPU memory estimator with at least one model profile
- compared two different precision or context configurations
- rendered the Kubernetes GPU workload examples
- written a short note about node pool design for development versus production

## Step 1 - Estimate Weight and KV Cache Memory

From the repository root:

```bash
python modules/06-gpu-and-accelerators/tools/gpu_memory_estimator.py --parameters-billions 7 --precision fp16 --layers 32 --hidden-size 4096 --batch-size 4 --context-tokens 4096
```

## Step 2 - Compare A More Aggressive Profile

Run the estimator again with a longer context window or larger batch size and compare the output.

## Step 3 - Render The GPU Workload Examples

```bash
kubectl kustomize platform/kubernetes/gpu-workloads
```

Inspect the different workload shapes:

- inference deployment
- batch embeddings job
- GPU smoke-check pod

## Step 4 - Reflection

Write down:

- which term changed memory pressure most in your examples
- what would make development, staging, and production node pools different
- which GPU metrics you would alert on first