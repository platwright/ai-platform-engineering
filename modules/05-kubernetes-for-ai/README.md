# Module 05 - Kubernetes For AI

## Overview

This module moves the containerized sample chat stack into Kubernetes. The goal is not to turn the course into generic Kubernetes training. The goal is to show how AI application and supporting workloads map onto core Kubernetes objects.

The same stack from Module 04 becomes Deployments, Services, a Job, a StatefulSet, ConfigMaps, a Secret template, an HPA, and an Ingress.

## Learning Objectives

By the end of this module, you should be able to:

- explain when Kubernetes is useful for AI workloads and when it is unnecessary
- map AI workloads onto Deployments, Jobs, StatefulSets, Services, and Ingress
- reason about scheduling and autoscaling for AI workloads
- describe networking requirements for user-facing and model-facing traffic
- explain how storage concerns differ for stateless applications and stateful backing services
- render and optionally deploy the sample chat Kubernetes stack

## Prerequisites

- Completion of [modules/04-containers-and-ai-workloads/README.md](../04-containers-and-ai-workloads/README.md)
- Familiarity with basic Kubernetes concepts
- `kubectl` installed
- `kind` or `k3d` recommended for the full lab path

## Difficulty And Time

- Difficulty: Intermediate
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [Why Kubernetes for AI?](chapters/01-why-kubernetes-for-ai.md)
2. [AI Workload Deployment](chapters/02-ai-workload-deployment.md)
3. [Scheduling AI Workloads](chapters/03-scheduling-ai-workloads.md)
4. [Autoscaling](chapters/04-autoscaling.md)
5. [Batch AI Jobs](chapters/05-batch-ai-jobs.md)
6. [Kubernetes Networking for AI](chapters/06-kubernetes-networking-for-ai.md)
7. [Storage for AI Workloads](chapters/07-storage-for-ai-workloads.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Runtime Assets

- [platform/kubernetes/sample-chat/README.md](../../platform/kubernetes/sample-chat/README.md)
- [applications/sample-chat/README.md](../../applications/sample-chat/README.md)
- [projects/project-01-model-api/README.md](../../projects/project-01-model-api/README.md)

## Expected Outcome

At the end of this module, you should have:

- a rendered Kubernetes stack for the sample chat application
- a clear mapping from AI workload types to Kubernetes resources
- a practical understanding of why stateful AI backing services need different treatment than stateless app pods
- notes on how autoscaling, networking, and storage change once the application moves into a cluster

## Knowledge Check

1. Why is Kubernetes a good fit for some AI workloads but not automatically the right answer for all of them?
2. Why does the sample chat stack use both Deployments and a StatefulSet?
3. Why do readiness and liveness probes matter for AI-facing services?
4. What is the difference between scaling a user-facing Deployment and a background Job?
5. What Kubernetes object would you use for mutable vector store persistence, and why?
6. Why can AI networking requirements differ from ordinary CRUD-style APIs?

## Common Mistakes

- treating all AI workloads as long-running HTTP Deployments
- forgetting that backing services introduce storage and state concerns
- skipping health probes and then misdiagnosing rollout issues
- assuming autoscaling policies for ordinary web traffic map directly onto AI workloads
- putting every workload on Kubernetes before confirming it belongs there

## Production Considerations

- cluster usage should follow workload shape, not hype
- StatefulSets and PVCs matter as soon as you care about vector stores and persistence
- Service and Ingress choices affect timeouts and user-facing latency
- readiness, liveness, and resource policy are part of operational design, not afterthoughts

## Next Step

Use [lab.md](lab.md) with [platform/kubernetes/sample-chat/README.md](../../platform/kubernetes/sample-chat/README.md) to render and inspect the stack.# Module 05 - Kubernetes For AI

Status: Planned

This module will focus on AI-specific Kubernetes usage rather than generic Kubernetes fundamentals.

Planned topics:

- why Kubernetes for AI
- workload deployment patterns
- scheduling AI workloads
- autoscaling
- batch AI jobs
- AI networking and storage