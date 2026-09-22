# Interview Guide

Practice these questions before technical interviews for AI platform engineering roles. Record your answers in `my-notes/capstone-interview-prep.md`.

A strong answer uses concrete examples from what you built rather than generic statements about best practices.

---

## Architecture Questions

### Q1: Walk me through the architecture of an AI platform you have worked on.

**What interviewers want**: a structured narrative that shows you understand the whole system, not just individual components.

**Rubric**:
- ✓ Covers at least: application layer, gateway, model serving, and one shared capability (RAG or agents)
- ✓ Explains the rationale for the layered design, not just describes it
- ✓ Mentions at least one operational concern (observability, security, or cost) alongside the capability discussion
- ✗ Describes only the happy path without any failure or operational awareness
- ✗ Gives only tool names without explaining what problem each solves

**Your preparation note**: *(write your own 3-minute version)*

---

### Q2: Why would you use a centralized AI gateway instead of letting each application call model providers directly?

**Rubric**:
- ✓ At least 3 concrete reasons (e.g., credential management, rate limiting, usage tracking, fallback)
- ✓ Explains a tradeoff or cost of the gateway approach
- ✓ Connects to real operational concerns rather than abstract principles
- ✗ Describes the gateway only as a proxy without explaining the platform value

---

### Q3: How would you design a multi-tenant RAG platform?

**Rubric**:
- ✓ Explicitly addresses tenant isolation at the retrieval layer (not just ingestion)
- ✓ Covers lifecycle: create, ingest, query, update, delete
- ✓ Mentions at least one operational signal (freshness, zero-result rate)
- ✓ Addresses the indirect prompt injection risk from retrieved content
- ✗ Describes RAG without mentioning multi-tenancy

---

## Operations Questions

### Q4: How would you diagnose a situation where response quality degraded but there are no HTTP errors?

**Rubric**:
- ✓ Immediately identifies this as a quality failure, not a technical failure
- ✓ Describes the investigation starting points: recent prompt changes, model updates, RAG staleness
- ✓ Explains how evaluation pipelines provide the signal that HTTP metrics cannot
- ✓ Has a specific rollback procedure
- ✗ Starts with checking server CPU or memory

---

### Q5: Describe how you would build SLOs for an AI system.

**Rubric**:
- ✓ Defines at least one technical SLO (availability or latency) AND at least one quality SLO
- ✓ Explains how to measure the quality SLO (evaluation pipelines)
- ✓ Explains error budgets and what happens when the budget is exhausted
- ✓ Acknowledges non-determinism as a challenge for exact-threshold SLOs
- ✗ Defines only availability and latency SLOs without the quality dimension

---

## Security Questions

### Q6: What is prompt injection and how do you defend against it in a platform context?

**Rubric**:
- ✓ Correctly distinguishes direct injection (user input) and indirect injection (via RAG documents)
- ✓ Names at least 3 defense layers (input validation, instruction isolation, output filtering, tool authorization)
- ✓ Explains why prompt injection cannot be fully prevented
- ✓ Frames it as a platform defense problem, not just a prompt engineering problem
- ✗ Suggests that "better system prompts" are the complete solution

---

### Q7: How do you secure an AI agent that can call external tools?

**Rubric**:
- ✓ Mentions least privilege for tool scope
- ✓ Describes approval gates for destructive actions
- ✓ Explains the audit trail requirement
- ✓ Addresses the confused deputy problem in multi-agent systems
- ✓ Distinguishes between the model's decision to call a tool and the platform's authorization to execute it

---

## Cost and Scaling Questions

### Q8: Our AI platform costs doubled month-over-month with no change in user traffic. What is your investigation plan?

**Rubric**:
- ✓ Checks per-request token counts (prompt length growth)
- ✓ Checks routing — did more traffic move to expensive models?
- ✓ Checks if `max_tokens` is missing and output length grew
- ✓ Checks for dev/staging environments running expensive models unnecessarily
- ✓ Checks evaluation runs: did eval frequency increase?

---

### Q9: When would you choose to self-host a model versus using a hosted API?

**Rubric**:
- ✓ Addresses data privacy as a primary consideration
- ✓ Addresses volume / cost break-even
- ✓ Acknowledges operational burden of self-hosting
- ✓ Mentions the capability gap (open-weight vs frontier)
- ✓ Describes the hybrid strategy (route by sensitivity, capability, and cost)

---

## Soft Questions

### Q10: You are joining a new organization as an AI platform engineer. What do you assess in the first 30 days?

**Strong answer framework**:

1. Understand the users: talk to 5 application developers about what works and what does not
2. Audit the current state: what does model access, retrieval, security, and cost management look like today?
3. Identify the biggest pain point: what is causing the most toil or blocking the most work?
4. Review the failure history: what incidents have occurred and what patterns do they reveal?
5. Map the roadmap to the organization's priorities: what is actually important vs what is interesting?

**What distinguishes a great answer**: the candidate talks to developers first, before touching infrastructure. They understand the user problem before proposing solutions.

---

## Final Preparation Checklist

Before your interview:

- [ ] You can draw the full platform architecture from memory in under 3 minutes
- [ ] You have a specific example for every quality claim ("we improved TTFT by X%", "we reduced cost by Y%")
- [ ] You can explain 5 design decisions and the tradeoffs involved in each
- [ ] You have a concrete answer for "what would you do differently?"
- [ ] You can describe a real incident or failure and what you learned from it
