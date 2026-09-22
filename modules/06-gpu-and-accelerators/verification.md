# Module 06 Verification

## Required Checks

Run the memory estimator:

```bash
python modules/06-gpu-and-accelerators/tools/gpu_memory_estimator.py --parameters-billions 7 --precision fp16 --layers 32 --hidden-size 4096 --batch-size 4 --context-tokens 4096
```

Expected result:

- weight memory estimate
- KV cache estimate
- total estimate with headroom

Render the GPU examples:

```bash
kubectl kustomize platform/kubernetes/gpu-workloads
```

Expected result:

- namespace and workload examples render successfully

## Understanding Check

You should be able to explain:

- why GPU memory is a primary constraint
- how precision affects deployment feasibility
- how Kubernetes placement policy interacts with accelerator availability
- why node pool separation matters
- which metrics indicate that a GPU-backed service is unhealthy or under-provisioned