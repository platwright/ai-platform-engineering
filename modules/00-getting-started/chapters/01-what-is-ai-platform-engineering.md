# Chapter 0.1 - What Is AI Platform Engineering?

## The Short Definition

AI platform engineering is the practice of building the shared systems, workflows, guardrails, and runtime foundations that let many teams build AI applications safely and repeatedly.

The job is usually not to create a novel model. The job is to make AI usable in an organization.

## Adjacent Roles And Overlap

| Role | Main focus | Where it overlaps with AI platform engineering |
| --- | --- | --- |
| AI Engineer | product-facing AI features | prompt design, orchestration, tool use, model integration |
| ML Engineer | model training and model lifecycle | model packaging, inference interfaces, evaluation pipelines |
| MLOps Engineer | ML delivery and operations | CI/CD, model promotion, experiment-to-production workflows |
| AI Platform Engineer | reusable platform capabilities | the central role in this course |
| Platform Engineer | internal developer platforms | self-service patterns, golden paths, abstractions |
| SRE | reliability and operational excellence | SLOs, incidents, observability, failure handling |
| Cloud Engineer | cloud runtime and services | infrastructure, identity, networking, and cost |

## What Makes The Role Distinct

An AI platform engineer cares about how AI workloads behave at scale.

That includes:

- model API standardization
- hosted versus self-hosted model choices
- vector and retrieval platforms
- tracing of prompts, tools, and model calls
- guardrails and policy
- secrets, identity, and tenancy
- latency, throughput, and cost behavior

## The Three Layers

### AI Application Layer

Where product behavior lives:

- chat UX
- business workflows
- tool selection
- application logic

### AI Platform Layer

Where reusable capabilities live:

- AI gateway
- retrieval platform
- agent runtime controls
- prompt and evaluation workflows
- observability and policy layers

### Infrastructure Layer

Where execution and shared foundations live:

- containers
- Kubernetes
- GPUs
- networking
- storage
- identity and secrets foundations

## What This Course Does Not Try To Do

This repository does not try to turn you into a data scientist or a deep learning researcher. It teaches enough AI to reason about the systems you need to operate.

## Why This Matters

If your mental model stops at "the app calls an LLM," you will struggle to design reliable AI systems. Platform work starts when you ask what happens when latency spikes, retrieval fails, costs explode, a provider rate-limits you, or one team needs different controls than another.