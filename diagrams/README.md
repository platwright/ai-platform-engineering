# Diagrams

This directory holds exported architecture diagrams and visual assets for the course.

Inline diagrams using Mermaid syntax are embedded directly in module files. This directory holds standalone diagram files for cases where a standalone image or higher-resolution export is useful.

## Planned Diagrams

### Platform Architecture

- [platform-overview.png](./platform-overview.png) — full Acme AI platform with all layers (application, gateway, RAG, agents, model serving, infrastructure, observability, developer portal)
- [platform-evolution.png](./platform-evolution.png) — sequence of platform stages from Module 03 through Module 17

### Module-Specific

- [rag-pipeline.png](./rag-pipeline.png) — end-to-end RAG pipeline from document ingest through grounded generation
- [agent-loop.png](./agent-loop.png) — agent control loop with tool execution, approval gate, and state transitions
- [model-serving-layers.png](./model-serving-layers.png) — model artifact, server, API surface, Kubernetes, and GPU layers
- [gateway-routing.png](./gateway-routing.png) — AI gateway routing decisions with fallback and rate limiting
- [token-context-budget.png](./token-context-budget.png) — context window composition and budget allocation visualization
- [kv-cache-memory.png](./kv-cache-memory.png) — KV cache memory layout and the effect of context length on concurrency

### Operations

- [failure-taxonomy.png](./failure-taxonomy.png) — AI platform failure taxonomy organized by layer
- [latency-decomposition.png](./latency-decomposition.png) — end-to-end latency waterfall from client to model and back
- [cost-attribution.png](./cost-attribution.png) — cost attribution flow from individual requests to per-tenant reports

## Contributing Diagrams

Diagrams should be:

- exported as PNG at 1920×1080 minimum resolution for platform overviews
- stored with the source file (`.drawio`, `.excalidraw`, or similar) alongside the export
- referenced from the relevant module `architecture.md` file

Mermaid diagrams embedded in Markdown are preferred for diagrams that are simple enough to represent accurately in code, as they render correctly in GitHub and VS Code without separate image files.
