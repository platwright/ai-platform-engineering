# Module 07 Architecture

## Serving Stack View

```mermaid
flowchart LR
    Client[Application or Benchmark] --> API[OpenAI-Compatible Inference API]
    API --> Server[vLLM Model Server]
    Server --> Model[Open Model Weights]
    Server --> GPU[GPU Memory and Compute]
    Server --> Metrics[Latency and Throughput Signals]
```

## Request Processing View

```mermaid
flowchart LR
    Prompt[Prompt] --> Prefill[Prefill Phase]
    Prefill --> KV[KV Cache]
    KV --> Decode[Decode Loop]
    Decode --> Tokens[Output Tokens]
```

## Kubernetes View

```mermaid
flowchart TB
    Ingress[Ingress or Port Forward] --> Service[vLLM Service]
    Service --> Deployment[vLLM Deployment]
    Deployment --> GPUNode[GPU Node]
    Benchmark[Project 02 Benchmark] --> Service
```

## What To Notice

- the serving path is a runtime system, not only an API contract
- performance behavior depends on both model properties and serving strategy
- Kubernetes gives deployment structure, but it does not remove the need to understand inference behavior