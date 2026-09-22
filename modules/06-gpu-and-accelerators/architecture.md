# Module 06 Architecture

## Accelerator-Aware Serving View

```mermaid
flowchart LR
    Request[Inference Request] --> Server[Model Server]
    Server --> GPU[GPU Memory and Compute]
    GPU --> Output[Generated Tokens]
```

## Memory Pressure Model

```mermaid
flowchart TB
    Weights[Model Weights]
    KV[KV Cache]
    Activations[Runtime Activations]
    Batch[Batch Size]
    Context[Context Length]

    Weights --> GPUMem[GPU Memory Budget]
    KV --> GPUMem
    Activations --> GPUMem
    Batch --> KV
    Context --> KV
```

## Kubernetes GPU Placement View

```mermaid
flowchart LR
    Pod[GPU Workload Pod] --> Scheduler[Kubernetes Scheduler]
    Scheduler --> GPUNode[GPU Node Pool]
    GPUNode --> Device[GPU Device]
    Pod --> Metrics[GPU and App Telemetry]
```

## What To Notice

- memory pressure is a serving concern, not only a model-training concern
- node pools and scheduling policy become part of application reliability once GPUs appear