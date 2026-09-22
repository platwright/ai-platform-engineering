# Module 03 - AI Application Architecture

## Overview

This module explains what an AI application looks like before containers, Kubernetes, GPUs, and model-serving platforms enter the picture. That is an important step. Platform engineers cannot operate systems well if they do not understand what the application layer is actually doing.

The module focuses on the application surfaces that sit between users and models: the API boundary, prompt layer, provider abstraction, state handling, configuration, and workload patterns. It uses Project 01 as the concrete implementation surface.

## Learning Objectives

By the end of this module, you should be able to:

- describe the major layers inside a production-oriented AI application
- distinguish stateless and stateful AI application patterns
- decide when an AI workload should be synchronous or asynchronous
- identify what belongs in configuration versus code
- adapt twelve-factor application principles to AI systems
- explain why a unified model client is a useful application abstraction
- run Project 01 and observe how one application interface can call multiple model providers

## Prerequisites

- Completion of [modules/01-ai-foundations/README.md](../01-ai-foundations/README.md)
- Familiarity with Python, JSON, and HTTP basics
- A working Python installation

You do not need Module 02 to complete this module, but later LLM-specific terminology will feel easier once Module 02 exists.

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 5 to 7 hours

## Module Map

### Chapters

1. [Anatomy of an AI Application](chapters/01-anatomy-of-an-ai-application.md)
2. [Stateless vs Stateful AI Applications](chapters/02-stateless-vs-stateful-ai-applications.md)
3. [Synchronous vs Asynchronous Workloads](chapters/03-synchronous-vs-asynchronous-workloads.md)
4. [AI Application Configuration](chapters/04-ai-application-configuration.md)
5. [Twelve-Factor Principles for AI Applications](chapters/05-twelve-factor-principles-for-ai-applications.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)
- [Associated Project: Unified Model Client](../../projects/project-01-model-api/README.md)

## Expected Outcome

At the end of this module, you should have:

- a clear application-layer architecture for AI systems in your head
- a concrete understanding of where prompts, models, routing, config, and state belong
- a working unified model client that can switch providers behind one interface
- notes about where your current applications are too coupled to a single model or provider

## Knowledge Check

1. Why should an AI application separate prompt handling from transport and provider adapters?
2. What kinds of state should stay inside the request path, and what kinds should move to explicit backing services?
3. Why is chat usually synchronous while indexing is usually asynchronous?
4. Which AI settings belong in configuration and which should stay in code?
5. How do twelve-factor ideas change when prompts, models, and evals become production artifacts?
6. Why is a unified model client useful even before an organization builds a full AI gateway?

## Common Mistakes

- hard-coding one provider API directly into application logic
- mixing prompt text, provider transport, and business logic in the same function
- storing conversational or retrieval state implicitly in the web tier
- treating synchronous and asynchronous AI paths as interchangeable
- placing secrets, model IDs, or prompt variants in code instead of configuration

## Production Considerations

- model provider abstractions should stabilize the application surface even if backends change
- prompts are operational artifacts and should be versioned and reviewed
- state management affects scaling, caching, tenancy, and privacy boundaries
- configuration drift can change application behavior as much as code changes can
- user-facing AI paths need latency and error handling designed up front

## Next Step

Read [concepts.md](concepts.md), then the chapter files, then build [Project 01](../../projects/project-01-model-api/README.md) through [lab.md](lab.md).