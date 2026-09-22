# Roadmap

## Goal

Build a free, public course repository that takes learners from AI platform fundamentals to a production-oriented internal AI platform narrative. The course should be practical, opinionated, and durable — meaning it remains useful as individual tools change because it teaches concepts before products.

## Delivery Phases

### Phase 1 - Foundation (Complete)

- repository structure and course narrative
- course guide, prerequisites, and contributor guidance
- Module 00 — Getting Started

### Phase 2 - Foundational Learning Path (Complete)

- Module 01 — AI Foundations
- Module 02 — LLM Foundations
- Module 03 — AI Application Architecture
- Project 01 — Unified Model Client

### Phase 3 - Platform Runtime (Complete)

- Module 04 — Containers and AI Workloads
- Module 05 — Kubernetes for AI
- Module 06 — GPU and Accelerators
- Module 07 — Model Serving
- Project 02 — Open Model Serving on Kubernetes

### Phase 4 - Shared Platform Capabilities (Complete)

- Module 08 — AI Gateway
- Module 09 — RAG Platform
- Module 10 — Agent Platform
- Project 03 — RAG as a Service
- Project 04 — Safe Agent Platform

### Phase 5 - Production Operations (Complete)

- Module 11 — LLMOps ✔ Complete
- Module 12 — Observability ✔ Complete
- Module 13 — AI Platform Security ✔ Complete
- Module 14 — Reliability ✔ Complete
- Module 15 — Scaling and Performance ✔ Complete
- Module 16 — AI FinOps ✔ Complete

### Phase 6 - Platform Productization (Complete)

- Module 17 — Developer Platform ✔ Complete
- Module 18 — Capstone ✔ Complete
- Final AI Platform project ✔ Complete

## Module Status

| Module | Status |
| --- | --- |
| 00 - Getting Started | Complete |
| 01 - AI Foundations | Complete |
| 02 - LLM Foundations | Complete |
| 03 - AI Application Architecture | Complete |
| 04 - Containers and AI Workloads | Complete |
| 05 - Kubernetes for AI | Complete |
| 06 - GPU and Accelerators | Complete |
| 07 - Model Serving | Complete |
| 08 - AI Gateway | Complete |
| 09 - RAG Platform | Complete |
| 10 - Agent Platform | Complete |
| 11 - LLMOps | Complete |
| 12 - Observability | Complete |
| 13 - AI Platform Security | Complete |
| 14 - Reliability | Complete |
| 15 - Scaling and Performance | Complete |
| 16 - AI FinOps | Complete |
| 17 - Developer Platform | Complete |
| 18 - Capstone | Complete |

## Short-Term Priorities

1. ~~Add failure labs: provider timeout and RAG staleness scenarios in `labs/failure-labs/`.~~ Done — `provider-timeout` and `rag-staleness` labs added.
2. ~~Add Backstage skeleton template files to `platform/backstage/templates/`.~~ Done — `new-rag-app` template added with catalog entries for gateway, RAG, and agent platform.
3. ~~Add a `python-ai-snippets.md` cheatsheet.~~ Done — added to `cheatsheets/python-ai-snippets.md`.
4. ~~Build and validate the capstone assembly end-to-end and update the assembly checklist.~~ Done — capstone artifacts complete in `modules/18-capstone/`.
5. ~~Scan all internal markdown links for broken references across the full module set.~~ Done — duplicate content removed from Module 18 README, solutions index updated.

## Next Priorities

1. Add actual diagram files to `diagrams/` — start with `platform-overview` and `rag-pipeline` as Mermaid exports.
2. Add starter lab scripts to `labs/starter/` — at minimum `token-counter.py` and `provider-switcher.py`.
3. Add GitOps Flux alternative to `platform/gitops/` alongside the existing ArgoCD manifests.
4. Add `platform/backstage/templates/new-rag-service/` golden path template for registering a RAG service.
5. Add agent-tool-escape failure lab to `labs/failure-labs/`.

## Content Maturity Principles

Each completed module should satisfy:

- **Concept-first**: learners understand why before they touch tools
- **Runnable**: every lab step produces a visible, verifiable outcome
- **Connected**: the module builds on previous modules and connects to later ones
- **Production-aware**: failure modes, observability, security, and cost are addressed
- **Checkable**: knowledge check questions and verification steps are present and honest
- **Concise**: no filler — every sentence should inform a platform engineering decision

## What This Course Is Not

This course is not:

- a data science or ML engineering curriculum
- a cloud provider tutorial (AWS, GCP, Azure)
- a prompt engineering guide
- a survey of every AI tool
- a replacement for deep Kubernetes or infrastructure training (Modules 04–06 teach enough to be effective, not everything)
