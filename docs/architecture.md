# Course Architecture

## Central Project

The course is organized around a fictional company called Acme AI that is building an internal AI platform for multiple application teams.

## Platform Direction

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

    Platform --> Support[Identity, Secrets, Evals, GitOps, CI/CD, Tracing, Metrics, Logging, Cost, Policy, SLOs]
```

## Diagram References

The course uses the exported architecture images in the repository to reinforce the system view across modules:

- [Platform overview](../diagrams/platform-overview.png)
- [Platform evolution](../diagrams/platform-evolution.png)
- [RAG pipeline](../diagrams/rag-pipeline.png)
- [Agent loop](../diagrams/agent-loop.png)
- [Gateway routing](../diagrams/gateway-routing.png)
- [Latency decomposition](../diagrams/latency-decomposition.png)
- [Failure taxonomy](../diagrams/failure-taxonomy.png)

## Why This Matters

The repository is intentionally not a collection of unrelated tutorials. Every module adds another capability to the same platform story so learners can reason about interfaces, ownership, and production tradeoffs.

## Stage Progression

1. Single application calling a model API
2. AI gateway and model routing
3. RAG as a reusable platform capability
4. Agents, tools, and MCP-aware operations
5. Kubernetes, GPUs, and self-hosted serving
6. Observability, evaluation, and security controls
7. Developer self-service platform experiences