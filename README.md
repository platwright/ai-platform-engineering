# AI Platform Engineering

Build the platform that AI engineers deploy on.

This repository is a hands-on, self-paced course for building and operating production AI platforms. It is designed for engineers who need to understand how AI workloads are developed, deployed, served, observed, secured, and scaled without turning the course into a data science curriculum.

## Who This Is For

- Platform Engineers
- DevOps Engineers
- SREs
- Cloud Engineers
- Kubernetes Engineers
- Infrastructure Engineers
- Software Engineers moving into AI infrastructure
- Architects who want practical AI platform knowledge

You do not need to be a machine learning engineer or data scientist to use this course.

## What You Will Build

The course follows a fictional company, Acme AI, as it builds an internal AI platform for multiple product teams. The platform evolves in stages:

1. Application -> Model API
2. Application -> AI Gateway -> Models
3. Application -> Gateway -> RAG -> Model
4. Agents -> Tools/MCP -> Models
5. Kubernetes -> GPU -> Model Serving
6. Observability + Evaluations + Security
7. Developer Self-Service Platform

By the end, you should be able to explain not only how these systems work, but how they fail, how to observe them, how to secure them, and how to operate them in production.

## Course Principles

- Concept before product: understand the platform capability before learning a specific tool.
- Local first: start with Docker, Python, local Kubernetes, and open tooling before optional cloud or GPU expansions.
- Build progressively: one platform grows across the course instead of many disconnected demos.
- Failure-aware learning: several labs deliberately create failure modes and recovery work.
- Production thinking: every major topic includes observability, security, scale, and cost.

## Start Here

1. Read [docs/course-guide.md](docs/course-guide.md).
2. Review [docs/prerequisites.md](docs/prerequisites.md).
3. Complete [modules/00-getting-started/README.md](modules/00-getting-started/README.md).
4. Complete [modules/01-ai-foundations/README.md](modules/01-ai-foundations/README.md).
5. Run the setup checks from [scripts/setup/check-prereqs.ps1](scripts/setup/check-prereqs.ps1) or [scripts/setup/check-prereqs.sh](scripts/setup/check-prereqs.sh).
6. Create your personal workbook using [scripts/setup/init-workbook.ps1](scripts/setup/init-workbook.ps1) or [scripts/setup/init-workbook.sh](scripts/setup/init-workbook.sh).

## Current Status

- Foundation scaffolding: complete
- Module 00 - Getting Started: complete
- Module 01 - AI Foundations: complete
- Module 02 - LLM Foundations: complete
- Module 03 - AI Application Architecture: complete
- Module 04 - Containers and AI Workloads: complete
- Module 05 - Kubernetes for AI: complete
- Module 06 - GPU and Accelerators: complete
- Module 07 - Model Serving: complete
- Module 08 - AI Gateway: complete
- Module 09 - RAG Platform: complete
- Module 10 - Agent Platform: complete
- Module 11 - LLMOps: complete
- Module 12 - Observability: complete
- Module 13 - AI Platform Security: complete
- Module 14 - Reliability: complete
- Module 15 - Scaling and Performance: complete
- Module 16 - AI FinOps: complete
- Module 17 - Developer Platform: complete
- Module 18 - Capstone: complete
- Project 01 - Unified Model Client: complete
- Project 02 - Open Model Serving on Kubernetes: complete
- Project 03 - RAG As A Service: complete
- Project 04 - Agent Platform: complete

## Initial Repository Shape

```text
ai-platform-engineering/
├── docs/
├── modules/
├── scripts/
├── labs/
├── projects/
├── platform/
├── applications/
├── diagrams/
├── cheatsheets/
└── solutions/
```

Later modules will fill those areas with labs, reference architectures, platform assets, and sample applications.

## Recommended Learning Flow

If you are new to AI platform work, follow the modules in order. Module 00 establishes the role, tooling, and course narrative. Module 01 gives you the workload mental model. Module 02 explains how LLM inference actually works — tokenization, generation parameters, streaming, structured outputs, tool calling, and the hosted vs self-hosted tradeoff. Module 03 shows what an AI application looks like before it is containerized or moved into Kubernetes. Module 04 packages that application into a local stack, Module 05 moves the same stack into Kubernetes, Module 06 explains accelerators, Module 07 turns model serving into a real runtime concern, Module 08 introduces a shared AI gateway, Module 09 turns retrieval into a reusable platform capability, and Module 10 adds safe tool use and agent platform controls.

See [docs/learning-paths.md](docs/learning-paths.md) for role-specific sequences and time estimates.

## License

This repository uses the MIT License. See [LICENSE](LICENSE).
