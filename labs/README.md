# Labs

This directory holds reusable labs that reinforce and extend the module material. Labs here are organized by complexity and by whether they are deliberately designed to create failure scenarios.

## Structure

- [starter/](starter/README.md) — beginner-friendly labs with minimal setup overhead
- [intermediate/](intermediate/README.md) — labs that combine multiple platform concepts
- [advanced/](advanced/README.md) — deeper labs for GPU, distributed inference, scaling, and multi-tenant behavior
- [failure-labs/](failure-labs/README.md) — intentional failure scenarios for diagnosis practice

## Completed Failure Labs

| Lab | Covers | Difficulty |
|---|---|---|
| [oom-lab](../platform/docker/oom-lab.compose.yml) | Module 04 — container resource limits | Starter |
| [provider-timeout](failure-labs/provider-timeout/README.md) | Modules 08, 14 — gateway fallback and reliability | Intermediate |
| [rag-staleness](failure-labs/rag-staleness/README.md) | Modules 09, 11, 14 — silent quality failure detection | Intermediate |

## How Labs Relate To Modules

Most hands-on practice happens directly in module `lab.md` files. The labs here are standalone extensions — they do not require completing a specific module first, but they reference relevant module concepts.

## Running A Lab

Each lab README has its own prerequisites and quick-start instructions. Labs that require a running stack will note which Docker Compose or Kubernetes assets to start first.

## Contributing A Lab

A good lab contribution includes:

- a clearly stated goal
- explicit prerequisites
- step-by-step instructions that produce a visible, verifiable outcome
- a reflection prompt to reinforce the concept
- a cleanup section if the lab creates persistent resources

See [CONTRIBUTING.md](../CONTRIBUTING.md) for general contribution guidance.
