# Course Guide

## Purpose

This course teaches the operational side of AI systems: the platform, reliability, security, delivery, and runtime concerns that appear once AI workloads move beyond prototypes.

The repository is intentionally built for practitioners who already know basic software and infrastructure fundamentals and need a structured path into AI platform engineering.

## How To Use This Repository

Each module follows a predictable flow so that you can learn quickly without re-learning the repository layout every time.

```text
Understand
  -> Visualize
  -> Build
  -> Verify
  -> Reflect
```

Most modules use these files:

- `README.md`: entry point, objectives, prerequisites, and navigation
- `concepts.md`: key ideas to understand before touching tools
- `architecture.md`: diagrams and system boundaries
- `lab.md`: hands-on work
- `challenge.md`: deeper practice without step-by-step guidance
- `verification.md`: checks to confirm your work
- `solution.md`: reference implementation or expected outputs
- `references.md`: external reading

## Learning Model

The course starts small and local, then grows into a production-oriented platform:

1. Understand AI workloads and the role of the platform engineer.
2. Learn how LLM and AI application behavior affects infrastructure.
3. Package workloads with containers and run them locally.
4. Move workloads into Kubernetes.
5. Add GPUs, model serving, routing, RAG, and agents.
6. Introduce observability, evaluation, security, and reliability engineering.
7. End with a self-service AI platform narrative.

## Your Workbook

You should treat your fork as a working notebook, not only as a repository copy.

Recommended personal directories:

- `progress/`: module-by-module progress logs
- `my-notes/`: concepts, diagrams, and decision notes
- `my-solutions/`: your own lab answers and experiments

You can create them with the setup scripts:

- [scripts/setup/init-workbook.ps1](../scripts/setup/init-workbook.ps1)
- [scripts/setup/init-workbook.sh](../scripts/setup/init-workbook.sh)

## Recommended Sequence

Start with:

1. [docs/prerequisites.md](prerequisites.md)
2. [modules/00-getting-started/README.md](../modules/00-getting-started/README.md)

Then move to later modules in order unless you already know the preceding area well.

## Expectations

You are not expected to memorize every tool or every Kubernetes resource. You are expected to build a clear mental model of how AI workloads behave and what that implies for platform design.

Every major area should leave you able to answer:

- How does this work?
- How does it fail?
- How do we observe it?
- How do we secure it?
- How do we scale it?
- How much does it cost?