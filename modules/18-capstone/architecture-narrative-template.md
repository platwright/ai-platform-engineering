# Architecture Narrative Template

Use this template to write your personal platform architecture narrative. Complete it in `my-solutions/capstone-architecture-narrative.md`.

A strong narrative answers: what problem did we solve, how did we solve it, what tradeoffs did we make, and what would we do differently?

---

## Section 1: The Problem

**The organization:** Acme AI is a company with multiple product teams that want to build AI-powered features. Before the platform existed, each team...

*(Complete: describe the fragmentation, duplication, and risk that the platform solves. Refer to Module 00 and Module 01 framing.)*

**Why a platform approach:** The alternative — each team managing its own model access, retrieval, agent tooling, security, and cost tracking — would produce...

*(Complete: quantify the cost of the alternative in engineering effort, security risk, or quality inconsistency.)*

---

## Section 2: The Platform We Built

**The platform provides these capabilities to application teams:**

1. *(Module 08)* AI Gateway — one stable endpoint for all model access, abstracting provider differences and enforcing policy
2. *(Module 09)* RAG Platform — managed retrieval-as-a-service with tenant isolation
3. *(Module 10)* Agent Platform — safe tool execution with authorization and approval gates
4. *(Modules 04–07)* Runtime — containerized workloads, Kubernetes scheduling, GPU-backed model serving
5. *(Modules 11–16)* Operations — LLMOps, observability, security, reliability, scaling, FinOps
6. *(Module 17)* Developer experience — catalog, templates, onboarding, governance

**The platform evolved in stages:**

```
Module 03: Single application calling a model directly
Module 04: Containerized application stack
Module 05: Kubernetes-based deployment
Module 06-07: GPU-backed self-hosted model serving
Module 08: AI gateway as the model access layer
Module 09: RAG as a shared platform service
Module 10: Agent platform with safe tool execution
Modules 11-16: Production operations across all dimensions
Module 17: Self-service developer experience
```

*(Add one sentence per stage describing what changed and why.)*

---

## Section 3: Key Design Decisions

**Decision 1: Why did we build a gateway instead of embedding provider logic in each application?**

We chose to build a centralized AI gateway because *(complete)*.

The alternative — each application managing its own provider logic — would have meant *(complete)*.

The tradeoff we accepted: *(complete)*.

**Decision 2: Why did we build RAG-as-a-service rather than letting each team own their retrieval?**

We chose a shared RAG platform because *(complete)*.

The tradeoff we accepted: *(complete)*.

**Decision 3: Why do agents require approval for destructive actions?**

We chose approval gates for destructive tools because *(complete)*.

The alternative — trusting the model's judgment for all actions — carries these risks: *(complete)*.

**Decision 4: Why did we start local-first rather than building on cloud infrastructure from the start?**

*(Complete: explain the reasoning from Module 00 and what it enabled.)*

*(Add decisions for any other areas you find significant — model selection, evaluation approach, team topology, etc.)*

---

## Section 4: What Would Need To Change For Production

**The local implementation deliberately simplifies these things:**

| Simplification | What Production Requires |
|---|---|
| Secrets in environment variables | Vault or external secrets operator |
| Single-replica serving | Multi-replica with autoscaling |
| Manual prompt deployment | CI/CD with eval gate |
| Local file-based RAG state | Managed vector database |
| Mock providers for development | Real hosted or self-hosted model endpoints |
| Basic logging | OpenTelemetry instrumentation |

*(Add your own observations from the operational review.)*

**The most important production change is:** *(complete — justify why you ranked it first)*

---

## Section 5: What I Would Carry Forward

**The three most valuable things I learned from building this platform:**

1.
2.
3.

**One thing I would do differently if starting over:**

**One question I still have about building AI platforms at scale:**
