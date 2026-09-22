# Helm Assets

This area will hold Helm charts and packaging examples for AI platform components.

## Planned Content

- `charts/ai-gateway/` — Helm chart for deploying the AI gateway service to Kubernetes
- `charts/rag-platform/` — Helm chart for the RAG platform service
- `charts/agent-platform/` — Helm chart for the agent platform service
- `charts/model-serving/` — Helm chart wrapping the vLLM deployment with sensible defaults
- `charts/observability-stack/` — Helm chart bundle for Prometheus, Grafana, and Jaeger

## Relationship To Modules

Helm packaging becomes relevant in Module 07 (Model Serving) and Module 08 (AI Gateway) when platform components need to be deployed repeatably to Kubernetes. Module 17 (Developer Platform) will use Helm charts as part of the golden path template for new AI services.

## Tool Version

All charts target Helm 3. They will use `helm.sh/chart` annotations and follow the official [Helm chart best practices](https://helm.sh/docs/chart_best_practices/).