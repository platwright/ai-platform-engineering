# Final AI Platform — Reference Architecture

## Complete Platform Diagram

```mermaid
flowchart TB
    subgraph "Developer Experience"
        Dev[Developer] --> Portal[Backstage Portal]
        Portal --> Catalog[Software Catalog]
        Portal --> Templates[Scaffolder Templates]
        Portal --> Docs[TechDocs]
    end

    subgraph "Applications"
        ChatApp[sample-chat\napplication]
        RAGApp[sample-rag\napplication]
        AgentApp[sample-agent\napplication]
    end

    subgraph "AI Platform Core"
        GW[AI Gateway\nRouting + Fallback\nRate Limiting + Cache\nUsage Tracking]
        RAGPlatform[RAG Platform\nIngestion + Retrieval\nReranking + Multi-tenant]
        AgentPlatform[Agent Platform\nTool Registry + Policy\nApproval Gates + Audit]
    end

    subgraph "Model Serving"
        ModelAPI[Project 01\nModel API\nProvider Abstraction]
        vLLM[vLLM\nSelf-hosted Serving\nOpenAI-compatible]
        Hosted[Hosted APIs\nOpenAI / Anthropic\nGemini / Cohere]
    end

    subgraph "Infrastructure"
        K8s[Kubernetes\nGPU Node Pools\nHPA / KEDA]
        GPU[GPU Hardware\nNVIDIA A10G / A100]
    end

    subgraph "Operations"
        OTel[OpenTelemetry\nCollector]
        Prom[Prometheus\n+ Grafana]
        Jaeger[Jaeger\nTracing]
        Eval[Evaluation\nPipelines]
    end

    Dev --> ChatApp
    Dev --> RAGApp
    Dev --> AgentApp
    Templates --> ChatApp

    ChatApp --> GW
    RAGApp --> GW
    AgentApp --> GW

    GW --> ModelAPI
    GW --> RAGPlatform
    GW --> AgentPlatform

    ModelAPI --> vLLM
    ModelAPI --> Hosted

    RAGPlatform --> VDB[(Vector\nDatabase)]
    AgentPlatform --> RAGPlatform
    AgentPlatform --> GW

    vLLM --> K8s
    K8s --> GPU

    GW --> OTel
    ModelAPI --> OTel
    RAGPlatform --> OTel
    AgentPlatform --> OTel

    OTel --> Prom
    OTel --> Jaeger
    Prom --> Grafana[Grafana\nDashboards]

    GW --> Eval
    Eval --> Prom
```

## Request Flow Diagrams

### Simple Chat Request

```mermaid
sequenceDiagram
    participant U as User
    participant App as sample-chat
    participant GW as AI Gateway
    participant M as Model API

    U->>App: POST /api/chat
    App->>GW: POST /api/chat (with tenant header)
    GW->>GW: authenticate + route
    GW->>M: POST /api/chat (selected provider)
    M-->>GW: response + usage
    GW-->>App: response + usage (logged)
    App-->>U: response text
```

### RAG-Augmented Request

```mermaid
sequenceDiagram
    participant U as User
    participant App as sample-rag
    participant GW as AI Gateway
    participant RAG as RAG Platform
    participant M as Model API

    U->>App: POST /api/chat
    App->>RAG: embed + retrieve (question)
    RAG-->>App: top-k chunks (reranked)
    App->>GW: POST /api/chat (question + context)
    GW->>M: forward with grounding prompt
    M-->>GW: grounded response
    GW-->>App: response
    App-->>U: response
```

### Agent Tool Execution

```mermaid
sequenceDiagram
    participant U as User
    participant Agent as Agent Platform
    participant GW as AI Gateway
    participant Tool as Tool Registry
    participant RAG as RAG Platform

    U->>Agent: POST /api/run (objective)
    Agent->>GW: plan (model selects tool)
    GW-->>Agent: tool_call: query_rag
    Agent->>Tool: authorize tool call
    Tool-->>Agent: authorized
    Agent->>RAG: execute query_rag
    RAG-->>Agent: retrieved context
    Agent->>GW: generate final response
    GW-->>Agent: response
    Agent-->>U: response + run artifact
```

## Component Ownership Map

| Component | Owner | Consumers |
|---|---|---|
| AI Gateway | Platform Team | All application teams |
| RAG Platform | Platform Team | Application teams, Agent Platform |
| Agent Platform | Platform Team | Application teams |
| Model API (Project 01) | Platform Team | Gateway, direct consumers |
| Model Serving (vLLM) | Platform Team | Model API |
| Evaluation Pipelines | Platform Team + App Teams | CI/CD, Observability |
| Application Templates | Platform Team | Application teams (read-only consumers) |
| Backstage Catalog | Platform Team | All developers |

## Environment Architecture

```
dev           → local Docker Compose stacks, mock providers, cheap model tier
staging       → Kubernetes (kind/k3d), real providers, cheap model tier
production    → Kubernetes (cloud), real providers + self-hosted, tiered routing
```
