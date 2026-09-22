# Platform Assets

This directory holds infrastructure and platform implementation assets used across the course. These assets are the runtime layer that the course modules deploy and operate.

## Structure

- [docker/](docker/README.md) — Docker Compose stacks for local application and platform service development
- [kubernetes/](kubernetes/README.md) — Kubernetes manifests for deploying the platform to a cluster
- [helm/](helm/README.md) — Helm charts for packaging and deploying platform components
- [gitops/](gitops/README.md) — GitOps configuration for declarative platform management
- [backstage/](backstage/README.md) — Developer portal configuration and catalog templates
- [terraform/](terraform/README.md) — Infrastructure-as-code for cloud provisioning
- [observability/](observability/README.md) — Telemetry configuration, dashboards, and alerting rules

## Relationship To Modules

| Asset Area | Primary Modules |
|---|---|
| docker/ | Module 04, Module 08, Module 09, Module 10 |
| kubernetes/ | Module 05, Module 06, Module 07 |
| helm/ | Module 07, Module 08, Module 17 |
| gitops/ | Module 11, Module 17 |
| backstage/ | Module 17 |
| terraform/ | Module 05 (optional cloud extension) |
| observability/ | Module 12 |