# Module 05 Solution

## Expected Outcome

A correct completion shows that you can map the existing application stack into Kubernetes without losing sight of workload boundaries.

## Manifest Interpretation

- Deployments represent long-running stateless application processes
- the Job represents asynchronous work
- the StatefulSet represents a persistent backing service
- the ConfigMap and Secret template externalize runtime behavior
- the HPA introduces controlled scaling for the user-facing tier

## The Important Lesson

The most important result is not that YAML exists. It is that each Kubernetes object now maps to a specific workload role you can explain.