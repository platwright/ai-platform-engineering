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
4. Run the setup checks from [scripts/setup/check-prereqs.ps1](scripts/setup/check-prereqs.ps1) or [scripts/setup/check-prereqs.sh](scripts/setup/check-prereqs.sh).
5. Create your personal workbook using [scripts/setup/init-workbook.ps1](scripts/setup/init-workbook.ps1) or [scripts/setup/init-workbook.sh](scripts/setup/init-workbook.sh).

## Current Status

- Foundation scaffolding: in progress
- Module 00 - Getting Started: complete
- Modules 01-18: planned

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

If you are new to AI platform work, follow the modules in order. If you already know container and Kubernetes fundamentals, Module 00 will help you align on scope, workflow, and the course architecture before you jump into later sections.

## License

This repository uses the MIT License. See [LICENSE](LICENSE).