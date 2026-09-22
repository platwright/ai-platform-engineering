# Module 04 Architecture

## Containerized Local Stack

```mermaid
flowchart LR
    User[User or curl] --> Chat[Sample Chat Container]
    Chat --> ModelAPI[Project 01 Model API Container]
    ModelAPI --> Mock[Mock or OpenAI-Compatible Provider]

    Chat --> Redis[Redis Cache Placeholder]
    Chat --> Qdrant[Qdrant Vector Store Placeholder]
    Chat --> Obs[Jaeger Placeholder]
```

## Image Boundary View

```mermaid
flowchart TB
    subgraph Application Image
        AppCode[Sample Chat Code]
        AppPrompts[Prompt Files]
        AppEntry[Serve or Request Entry Point]
    end

    subgraph Model API Image
        ModelCode[Unified Model Client]
        ModelPrompts[Prompt Files]
        ModelEntry[HTTP API Entry Point]
    end
```

## OOM Failure Lab

```mermaid
flowchart LR
    OOMLab[Memory Hog Container] --> Limit[64 MiB Memory Limit]
    Limit --> Failure[Container OOM / Process Kill]
    Failure --> Diagnose[Inspect logs and resource policy]
```

## What To Notice

- the application and model-access layers are networked services, not one process
- resource policies belong to the service definition, not only to human memory
- backing services can appear in the local stack even before the application uses every one directly