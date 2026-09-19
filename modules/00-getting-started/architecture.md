# Module 00 Architecture

## Why Start With Architecture In Module 00

Even before building anything, you need a stable mental model for the platform we are going to grow across the course.

The architecture begins very small and becomes more capable over time.

## Stage Evolution

```mermaid
flowchart TD
    S1[Stage 1<br/>Application -> Model API]
    S2[Stage 2<br/>Application -> AI Gateway -> Models]
    S3[Stage 3<br/>Application -> Gateway -> RAG -> Model]
    S4[Stage 4<br/>Agents -> Tools/MCP -> Models]
    S5[Stage 5<br/>Kubernetes -> GPU -> Model Serving]
    S6[Stage 6<br/>Observability + Evals + Security]
    S7[Stage 7<br/>Developer Self-Service Platform]

    S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
```

## Final Platform Direction

```mermaid
flowchart TD
    Devs[Developers] --> Portal[Developer Portal]
    Portal --> Templates[Templates]
    Portal --> APIs[Platform APIs]
    Templates --> Platform[Internal AI Platform]
    APIs --> Platform

    Platform --> Gateway[AI Gateway]
    Platform --> RAG[RAG Platform]
    Platform --> Agents[Agent Platform]

    Gateway --> Serving[Model Serving]
    RAG --> Serving
    Agents --> Serving

    Serving --> Hosted[Hosted Models]
    Serving --> SelfHosted[Self-hosted LLMs]
    SelfHosted --> GPU[GPU Infrastructure]
    GPU --> K8s[Kubernetes]

    Platform --> Support[GitOps, CI/CD, Identity, Secrets, Evals, Tracing, Metrics, Logging, Cost, Policy, SLOs]
```

## Layer Boundaries

```mermaid
flowchart TB
    subgraph Application Layer
        Chat[Sample Chat App]
        RagApp[Sample RAG App]
        AgentApp[Sample Agent App]
    end

    subgraph Platform Layer
        Gateway[AI Gateway]
        RagSvc[RAG Services]
        AgentSvc[Agent Runtime Controls]
        Obs[Observability and Evals]
    end

    subgraph Infrastructure Layer
        Compute[Compute and Containers]
        K8s[Kubernetes]
        GPU[GPU and Accelerators]
        Data[Storage and Networking]
    end

    Chat --> Gateway
    RagApp --> RagSvc
    AgentApp --> AgentSvc

    Gateway --> Compute
    RagSvc --> K8s
    AgentSvc --> GPU
    Obs --> Data
```

## What Module 00 Covers

Module 00 does not implement this platform yet. It gives you enough orientation to understand where each future capability fits and why the repository structure is being created the way it is.