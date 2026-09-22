# Module 05 Concepts

## Why This Module Exists

Kubernetes should only enter the course after the workload and container packaging are already clear. Otherwise learners end up deploying YAML without understanding what the workload needs.

## AI Workloads Map To Different Kubernetes Objects

The course uses a few core mappings:

- stateless user-facing APIs -> Deployment
- background one-off work -> Job
- stateful backing services -> StatefulSet
- service discovery -> Service
- external traffic entry -> Ingress or Gateway

## Scheduling And Resource Policy Still Matter Without GPUs

Even CPU-based early workloads need:

- requests and limits
- readiness and liveness checks
- rollout discipline
- clear service boundaries

Later GPU modules will extend that thinking rather than replace it.

## Storage Changes The Story

As soon as a workload owns durable state, the platform story changes. That is why the module includes a StatefulSet and persistent storage example even though the sample app itself stays largely stateless.

## Networking Is Part Of Runtime Behavior

User-facing chat traffic, internal model API traffic, and background job traffic do not all behave the same way. Kubernetes makes those paths explicit.