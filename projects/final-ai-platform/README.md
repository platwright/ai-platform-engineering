# Final AI Platform — Acme AI Reference Implementation

This project consolidates the entire Acme AI internal platform into a single reference. It is the companion to [modules/18-capstone/README.md](../../modules/18-capstone/README.md).

## What This Is

The final platform is the accumulated result of all modules and projects in this course: a local-first, production-aware AI platform with:

- A unified model API abstraction (Project 01)
- A containerized application stack (Module 04)
- Kubernetes-based deployment with GPU support (Modules 05–06)
- Self-hosted model serving via vLLM (Module 07 / Project 02)
- An AI gateway with routing, fallback, rate limiting, and usage tracking (Module 08)
- RAG as a platform service with multi-tenant isolation (Module 09 / Project 03)
- A safe agent platform with tool authorization and approval gates (Module 10 / Project 04)
- LLMOps with prompt versioning and evaluation pipelines (Module 11)
- Full observability: metrics, traces, logs, and evaluation-driven signals (Module 12)
- Defense-in-depth security covering prompt injection, secrets, and supply chain (Module 13)
- Reliability engineering: SLOs, fallback chains, and incident runbooks (Module 14)
- Scaling and performance: autoscaling, load testing, and inference optimization (Module 15)
- AI FinOps: cost attribution, routing economics, and chargeback (Module 16)
- Self-service developer experience via Backstage (Module 17)

## Project Files

- [architecture.md](architecture.md) — complete reference architecture
- [deployment-guide.md](deployment-guide.md) — step-by-step from-scratch deployment
- [operational-runbook.md](operational-runbook.md) — on-call runbook for common incidents
- [platform-decisions.md](platform-decisions.md) — design decision log with alternatives

## Quick Platform Start

**Step 1: Validate environment**
```bash
./scripts/setup/check-prereqs.sh
```

**Step 2: Start the gateway stack**
```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml up -d --build
```

**Step 3: Initialize RAG and verify**
```bash
python projects/project-03-rag-platform/app.py create-service \
  --service-name team-a-kb --tenant team-a \
  --docs-dir applications/sample-rag/example-docs/team-a

python projects/project-03-rag-platform/app.py ingest --service-name team-a-kb

curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is retrieval freshness?"}' | python -m json.tool
```

A JSON response with a non-empty `response` field confirms the platform is running.

## Platform Capabilities

| Capability | Component | Entry Point |
|---|---|---|
| Model API | Project 01 | `POST :8001/api/chat` |
| Chat application | sample-chat | `POST :8080/api/chat` |
| AI gateway | ai-gateway-stack | `POST :8080/api/chat` |
| RAG query | Project 03 | CLI or `POST :8081/api/query` |
| Agent runs | Project 04 | CLI or `POST :8082/api/run` |
| Evaluation | eval/run_eval.py | CLI |
| Cost report | eval/cost_report.py | CLI |
| Developer catalog | platform/backstage | Backstage portal |

## Production Readiness Gaps

This is a learning implementation. Before production:

| Gap | Production Requirement |
|---|---|
| Secrets in env vars | External secrets manager (Vault) |
| Single-replica serving | HPA/KEDA autoscaling with GPU pools |
| Local file-based state | Managed vector DB + cloud storage |
| Basic stdout logging | OpenTelemetry + aggregation stack |
| Manual prompt deployment | CI pipeline with eval gate + GitOps |
| No internal API auth | JWT/service account authentication |

## License

MIT. See [LICENSE](../../LICENSE).