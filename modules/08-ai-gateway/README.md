# Module 08 - AI Gateway

## Overview

This module turns model access into a shared, governed platform interface. Instead of every application embedding provider-specific logic, the gateway centralizes model routing, fallback, rate limiting, usage tracking, and caching behavior behind one endpoint.

The module uses a lightweight local AI gateway service that sits in front of Project 01 and makes those platform concerns visible.

## Learning Objectives

By the end of this module, you should be able to:

- explain why AI systems need a gateway layer
- describe the value of a unified model endpoint
- implement basic model routing and fallback behavior
- reason about rate limiting, quotas, and usage tracking
- distinguish prompt caching from semantic caching
- explain how Kubernetes inference routing relates to gateway design

## Prerequisites

- Completion of [modules/07-model-serving/README.md](../07-model-serving/README.md)
- Familiarity with Project 01 and the sample application stack

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 5 to 7 hours

## Module Map

### Chapters

1. [Why AI Needs a Gateway](chapters/01-why-ai-needs-a-gateway.md)
2. [Unified Model Endpoint](chapters/02-unified-model-endpoint.md)
3. [Model Routing](chapters/03-model-routing.md)
4. [Fallback and Resilience](chapters/04-fallback-and-resilience.md)
5. [Rate Limiting and Quotas](chapters/05-rate-limiting-and-quotas.md)
6. [Semantic and Prompt Caching](chapters/06-semantic-and-prompt-caching.md)
7. [Kubernetes Inference Routing](chapters/07-kubernetes-inference-routing.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [platform/docker/ai-gateway-service/app.py](../../platform/docker/ai-gateway-service/app.py)
- [platform/docker/ai-gateway-stack.compose.yml](../../platform/docker/ai-gateway-stack.compose.yml)
- [platform/kubernetes/ai-gateway/README.md](../../platform/kubernetes/ai-gateway/README.md)
- [projects/project-01-model-api/README.md](../../projects/project-01-model-api/README.md)

## Expected Outcome

At the end of this module, you should have:

- a working local AI gateway service with a unified `/api/chat` endpoint
- a practical understanding of route selection, fallback, rate limiting, caching, and usage metrics
- Docker Compose and Kubernetes assets for the gateway layer
- notes on how a later production gateway could extend the same ideas

## Knowledge Check

1. Why is a gateway more useful than embedding provider logic in every app?
2. What kinds of routing decisions belong in a gateway?
3. Why is fallback a resilience pattern but not a free lunch?
4. What is the difference between prompt caching and semantic caching?
5. Why should rate limiting be scoped to users, teams, apps, or tenants explicitly?
6. How does Kubernetes inference routing differ from ordinary HTTP ingress routing?

## Common Mistakes

- treating a gateway as only a proxy instead of a control point
- hiding route choices and fallback behavior so applications cannot reason about them
- using caching without clarity about correctness tradeoffs
- enforcing rate limits without useful usage visibility
- centralizing model access without centralizing policy and observability

## Production Considerations

- gateway policy affects cost, privacy, resilience, and developer experience
- fallback paths need monitoring because they can hide upstream failures
- caches should be measured for both hit rate and correctness risk
- unified endpoints simplify adoption only if governance remains visible and debuggable

## Next Step

Read [concepts.md](concepts.md), then run the local gateway assets through [lab.md](lab.md).