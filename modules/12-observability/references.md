# Module 12 References

## Observability Fundamentals

- [Observability Engineering (O'Reilly)](https://www.oreilly.com/library/view/observability-engineering/9781492076438/) — Majors, Fong-Jones, Miranda: authoritative practical guide
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/) — official OTel instrumentation reference
- [OpenTelemetry GenAI Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — standard span attributes for LLM calls
- [Prometheus Documentation](https://prometheus.io/docs/) — metrics collection and alerting reference
- [Grafana Documentation](https://grafana.com/docs/) — dashboard and alert configuration

## LLM-Specific Observability

- [OpenLLMetry](https://github.com/traceloop/openllmetry) — OpenTelemetry-based tracing for LLM calls, supports multiple providers
- [Helicone](https://www.helicone.ai/) — LLM observability proxy with cost tracking and tracing
- [LangSmith](https://docs.smith.langchain.com/) — LangChain tracing, evaluation, and monitoring
- [Phoenix (Arize)](https://github.com/Arize-ai/phoenix) — open-source LLM observability and evaluation

## Model Serving Metrics

- [vLLM Metrics Documentation](https://docs.vllm.ai/en/latest/serving/metrics.html) — vLLM Prometheus metrics reference
- [NVIDIA DCGM Exporter](https://github.com/NVIDIA/dcgm-exporter) — GPU metrics for Kubernetes
- [TGI Metrics](https://huggingface.co/docs/text-generation-inference/reference/metrics) — Text Generation Inference metrics

## Distributed Tracing

- [Jaeger Documentation](https://www.jaegertracing.io/docs/) — distributed tracing backend
- [Grafana Tempo](https://grafana.com/docs/tempo/) — distributed tracing with Grafana integration
- [W3C TraceContext Specification](https://www.w3.org/TR/trace-context/) — `traceparent` header standard

## Alerting and SLOs

- [The Site Reliability Workbook (Google)](https://sre.google/workbook/table-of-contents/) — SLO design and error budget management
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/) — Prometheus alert routing
- [SLO burn rate alerting](https://sre.google/workbook/alerting-on-slos/) — Google's burn rate alerting methodology

## Privacy in Observability

- [Privacy-Preserving Telemetry (CNCF)](https://www.cncf.io/blog/2022/08/03/privacy-preserving-telemetry-a-guide-to-protecting-sensitive-data/) — guidance on logging without PII exposure
- [GDPR and Logging](https://gdpr.eu/article-5-how-long-can-personal-data-be-stored/) — data minimization requirements relevant to log retention
