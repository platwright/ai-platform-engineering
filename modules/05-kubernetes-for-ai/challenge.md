# Module 05 Challenge

## Challenge Prompt

Acme AI wants the sample chat stack to support three environments:

- developer sandbox
- staging
- production

Design the Kubernetes workload policy for each environment.

## Deliverable

Create a note in:

- `my-solutions/module-05-kubernetes-strategy.md`

Include:

1. replica strategy
2. health-probe expectations
3. which resources need persistence
4. which workloads should autoscale
5. which ingress or gateway controls you would add first

## Extension

Describe how the manifest set would change if the model API moved from mock providers to a self-hosted model server that needed GPUs.