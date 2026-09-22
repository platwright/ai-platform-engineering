# Observability Assets

This area will hold telemetry configuration, dashboard definitions, tracing examples, and alerting rules for the AI platform observability stack.

## Planned Content

- `otel-collector-config.yaml` — OpenTelemetry Collector configuration that receives traces and metrics from AI workloads and routes them to Prometheus and Jaeger
- `prometheus/` — Prometheus scrape configurations and alerting rules for AI platform metrics
- `grafana/dashboards/ai-platform-overview.json` — Grafana dashboard covering gateway request rate, TTFT, token usage, error rate, and GPU utilization
- `grafana/dashboards/rag-platform.json` — Grafana dashboard for ingestion success, retrieval latency, and index freshness
- `grafana/dashboards/agent-platform.json` — Grafana dashboard for tool call rates, approval events, and agent run durations
- `jaeger/` — Jaeger deployment configuration for distributed tracing

## Compose Stack

A local observability stack will be provided as a Docker Compose profile that can be activated alongside the existing application stacks:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml \
  --profile observe up
```

## Relationship To Module 12

Module 12 (Observability) will use these assets in its lab to build end-to-end visibility into the AI platform stack. The assets here represent the infrastructure side; the instrumentation code will live in the application and platform service code.
