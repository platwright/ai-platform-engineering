# Final AI Platform — Design Decision Log

This document records the key architectural decisions made in building the Acme AI platform, including the alternatives considered and the reasoning for each choice.

---

## Decision 001: Centralized AI Gateway

**Decision**: Route all model traffic through a single AI gateway layer rather than having each application call model providers directly.

**Context**: Multiple application teams need model access. Without a gateway, each team manages its own provider credentials, rate limiting, fallback logic, and usage tracking separately.

**Alternatives considered**:
1. Each application embeds provider SDK — chosen rejected because it duplicates secrets management, rate limit logic, and usage tracking across every app
2. A shared library without a gateway service — rejected because libraries do not enforce policy at runtime; an app can bypass a library but cannot bypass a network call
3. A managed third-party gateway (e.g., Kong AI Gateway) — viable for production, but local-first learning objective requires owning the implementation

**Decision rationale**: The gateway as a platform service provides a single enforcement point for credentials, routing policy, rate limiting, fallback, usage tracking, and caching. Cost: one additional network hop; single point of failure if not made highly available.

**Module reference**: Module 08

---

## Decision 002: RAG as a Shared Platform Service

**Decision**: Provide RAG as a managed service with per-tenant isolation, rather than letting each application team build their own retrieval pipeline.

**Context**: Multiple teams need document-grounded AI responses. Without a shared service, each team would build its own ingestion, embedding, storage, and retrieval pipeline with overlapping code, different quality standards, and no cost aggregation.

**Alternatives considered**:
1. Each team builds their own RAG — rejected because it fragments quality, security, and cost; tenant isolation becomes each team's problem
2. A single shared RAG index with no tenant isolation — rejected due to data privacy and access control requirements
3. Fully managed external RAG (e.g., a vendor service) — viable for production, not suitable for a local-first learning implementation

**Decision rationale**: A shared service provides consistent quality controls, centralized cost attribution, and enforced tenant isolation while reducing the engineering burden on each application team. Cost: platform team owns the retrieval quality; application teams accept the abstraction.

**Module reference**: Module 09 / Project 03

---

## Decision 003: Approval Gates for Destructive Agent Actions

**Decision**: Require an explicit approval token before the agent platform executes any action classified as destructive (delete, scale-to-zero, revoke credentials).

**Context**: Agents that can call tools have the ability to take irreversible real-world actions. A successful prompt injection or a model planning error could trigger a destructive action without any human review.

**Alternatives considered**:
1. No approval requirement — rejected because the blast radius of a model error or injection is unacceptably high for destructive operations
2. Human-in-the-loop review for all tool calls — too slow for interactive use cases; frustrating for safe read-only operations
3. Approval based on tool output assessment — rejected because you cannot reliably assess impact before execution

**Decision rationale**: Requiring an approval token for destructive-class tools allows safe read-only operations to flow without friction while providing a meaningful gate for high-impact actions. Cost: destructive operations require out-of-band coordination; model cannot autonomously complete multi-step workflows that include destructive steps.

**Module reference**: Module 10 / Project 04

---

## Decision 004: Local-First Learning Path

**Decision**: Design the course to run on a developer laptop without cloud accounts, GPU hardware, or external services. Cloud and GPU paths are optional extensions.

**Context**: The course targets a global audience across different economic contexts. Requiring cloud accounts, GPU hardware, or paid model APIs creates financial and access barriers.

**Alternatives considered**:
1. Cloud-native from the start (Kubernetes on GKE, managed services) — rejected due to cost and access barriers; also removes the learning value of understanding the underlying components
2. GPU required from module 6 — rejected because GPU hardware is expensive and unavailable to many learners; abstract concept teaching remains valuable without hardware
3. Paid API required from module 1 — rejected because free tiers are unreliable and forcing payment gates out early learners

**Decision rationale**: Local-first ensures every learner can follow every conceptual module. GPU, cloud, and paid API paths are additive extensions that learners can explore when available. Cost: local implementations are simplified and not production-representative; learners must understand the gap.

**Module reference**: Module 00, applies throughout

---

## Decision 005: Prompt Versioning as Files in Git

**Decision**: Store prompt templates as versioned YAML files in the application repository rather than in a database or dedicated prompt management tool.

**Context**: Prompts need version control, review, and deployment discipline. Various tools exist (LangSmith, PromptLayer, etc.) but introduce external dependencies.

**Alternatives considered**:
1. Prompts embedded as strings in application code — rejected because they have no version history, no review process, and no stable identity
2. Dedicated prompt management tool (LangSmith) — viable for production; adds external dependency and account requirement for the course
3. Database-backed prompt registry — viable for production; adds infrastructure complexity beyond the course scope

**Decision rationale**: File-based versioning in git uses infrastructure every developer already understands. PR reviews for prompt changes are the same as PR reviews for code. Cost: no built-in eval tracking or promotion UI; these must be added for production use.

**Module reference**: Module 11

---

## Decision 006: LLM-as-Judge for Evaluation Scoring

**Decision**: Use a separate language model to evaluate open-ended RAG responses rather than exact-match or template-based scoring.

**Context**: RAG responses are open-ended. The same correct answer can be expressed in many valid ways. Exact-match scoring would fail most correct responses.

**Alternatives considered**:
1. Exact match — only works for structured output extraction; fails for conversational responses
2. Human evaluation for all cases — not scalable for CI pipelines; expensive
3. Keyword presence scoring — used as a low-cost preliminary filter but misses semantic correctness; a response that contains the right words in the wrong context still passes

**Decision rationale**: LLM-as-judge scales with the number of eval cases, provides nuanced assessment, and produces human-readable reasoning. Cost: judge model calls add cost and latency to the eval pipeline; the judge shares biases with the model under evaluation.

**Module reference**: Module 11

---

## Decision 007: Evaluation-Driven Observability as a First-Class Pillar

**Decision**: Treat automated evaluation scores as a fifth observability pillar alongside metrics, logs, traces, and events — not as a separate LLMOps concern.

**Context**: AI systems can be fully available and fast while producing poor-quality responses. Operational dashboards that show only availability and latency give false confidence.

**Alternatives considered**:
1. Quality is application teams' responsibility, not platform observability — rejected because quality signals belong in the platform's operational picture
2. Run evaluations only before releases, not continuously — insufficient; model drift and prompt regressions occur in production without a deployment trigger

**Decision rationale**: Including eval score trends in the platform dashboard creates a single source of operational truth that covers both the technical and quality dimensions of reliability. Cost: eval pipeline has ongoing cost; sampling strategies are needed to keep it affordable.

**Module reference**: Module 12 Chapter 08, Module 14
