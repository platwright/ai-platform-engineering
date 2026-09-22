# Module 04 - Containers And AI Workloads

## Overview

This module packages the first real application stack in the repository. The sample chat application and Project 01 model API move from local Python processes into container images and a local Docker Compose stack.

The goal is not only to run `docker build`. The goal is to understand what changes when AI applications become containerized workloads: image boundaries, prompt assets, resource limits, backing services, local stacks, and deliberate failure testing.

## Learning Objectives

By the end of this module, you should be able to:

- containerize an AI application and its model access layer separately
- explain why application images and model images have different concerns
- compare model storage patterns and their operational tradeoffs
- reason about CPU and memory limits for AI workloads
- run the sample chat stack locally with Docker Compose
- trigger and diagnose a deliberate container OOM failure

## Prerequisites

- Completion of [modules/03-ai-application-architecture/README.md](../03-ai-application-architecture/README.md)
- Familiarity with Docker basics
- Docker or Docker Desktop installed and working

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 5 to 7 hours

## Module Map

### Chapters

1. [Containerizing AI Applications](chapters/01-containerizing-ai-applications.md)
2. [Model Images vs Application Images](chapters/02-model-images-vs-application-images.md)
3. [Model Storage](chapters/03-model-storage.md)
4. [Container Resource Management](chapters/04-container-resource-management.md)
5. [Local AI Stack with Docker Compose](chapters/05-local-ai-stack-with-docker-compose.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Runtime Assets

- [applications/sample-chat/README.md](../../applications/sample-chat/README.md)
- [projects/project-01-model-api/README.md](../../projects/project-01-model-api/README.md)
- [platform/docker/README.md](../../platform/docker/README.md)

## Expected Outcome

At the end of this module, you should have:

- two working Dockerfiles for the application and model API layers
- a local Compose stack that runs the sample chat application end to end
- a concrete understanding of why AI runtime assets should be split by concern
- one deliberate OOM failure you can explain and diagnose

## Knowledge Check

1. Why is it useful to containerize the application API and the model access layer separately?
2. Why should model weights not automatically live inside a large application image?
3. What tradeoffs exist between local model caches, object storage, and persistent volumes?
4. Why do resource limits matter for AI workloads even before GPUs enter the picture?
5. What does Docker Compose teach that a single `docker run` command does not?
6. Why is a deliberate OOM lab useful to a platform engineer?

## Common Mistakes

- baking too many unrelated concerns into one container image
- hard-coding local addresses that break once services become networked containers
- assuming containerization alone solves configuration drift
- treating memory limits as optional rather than part of workload design
- skipping failure testing and only validating the happy path

## Production Considerations

- separate images make upgrades, rollback, and vulnerability management easier
- prompt assets and configuration need clear packaging rules
- local Compose stacks are useful mirrors of production concepts, not substitutes for production systems
- resource limits and health checks should be designed before incidents, not after them

## Next Step

Review [concepts.md](concepts.md), then use [lab.md](lab.md) with [platform/docker/README.md](../../platform/docker/README.md) to run the stack.# Module 04 - Containers And AI Workloads

Status: Planned

This module will move the course into packaging and running AI applications with container-native workflows.

Planned topics:

- containerizing AI applications
- model images versus application images
- model storage patterns
- resource requests and limits
- local AI stacks with Docker Compose
- OOM failure labs