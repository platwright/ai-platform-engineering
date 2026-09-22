# Terraform Assets

This area will hold infrastructure-as-code examples for cloud or platform provisioning scenarios.

## Planned Content

- `modules/gpu-node-pool/` — Terraform module for provisioning a GPU node pool (AWS, GCP, or Azure)
- `modules/managed-vector-db/` — Terraform module for provisioning a managed vector database
- `modules/ai-gateway-service/` — Terraform module for a cloud-managed AI gateway (optional)
- `examples/local-kind-cluster/` — OpenTofu/Terraform configuration for a local kind cluster with GPU simulator
- `examples/gke-ai-platform/` — reference architecture for GKE-based AI platform (planned for later modules)

## Relationship To Modules

Terraform assets will become relevant in later modules when the course moves from local-first exploration to production-oriented provisioning patterns. Module 05 (Kubernetes for AI) covers the concepts; the Terraform assets provide the IaC implementation.

## Tool Preference

The course prefers OpenTofu (the open-source Terraform fork) where possible to avoid licensing constraints. All configurations will be compatible with Terraform 1.5+ and OpenTofu 1.6+.
