# Chapter 1.4 - Foundation Models

## Why Foundation Models Matter To Platform Teams

Foundation models become a platform concern as soon as more than one team wants to use them. Then the organization needs shared decisions around access, routing, policy, observability, and cost controls.

## Proprietary Models

Proprietary models are closed offerings controlled by a vendor. You usually access them through an API or managed platform.

Typical strengths:

- fast adoption
- minimal infrastructure burden
- strong model quality in many cases

Typical tradeoffs:

- vendor dependency
- pricing exposure
- quota and outage exposure
- reduced control over internals

## Open-Weight Models

Open-weight models provide downloadable model weights that you can run yourself or through a third party.

Typical strengths:

- more control
- more deployment flexibility
- easier privacy boundary control

Typical tradeoffs:

- more operational burden
- hardware planning responsibility
- model serving engineering becomes your problem

## Hosted Models

Hosted models are consumed through an external provider or managed service. They may be proprietary or open-weight behind the scenes.

Hosted usage is often the fastest path for early teams, which is why many AI platforms start by standardizing access to hosted providers.

## Self-Hosted Models

Self-hosted models run on infrastructure you operate. That can mean local development, a private cloud, or a Kubernetes-based serving platform.

Self-hosting can help when you need:

- private deployment control
- lower marginal cost at high scale
- specific open models
- custom serving behavior

But it also means you own:

- scaling
- model loading
- GPU planning
- patching
- incident response

## Fine-Tuned Models

Fine-tuning adapts a base model for a narrower task or domain. That can improve behavior, but it adds lifecycle responsibilities around:

- artifact versioning
- evaluation
- rollback
- deployment compatibility

## A Practical Comparison

| Model strategy | Control | Speed to adopt | Operational burden | Privacy control |
| --- | --- | --- | --- | --- |
| Proprietary hosted | low to medium | high | low | medium |
| Open-weight hosted | medium | medium to high | low to medium | medium |
| Open-weight self-hosted | high | low to medium | high | high |
| Fine-tuned self-hosted | very high | lower | very high | high |

## Platform Takeaway

The job is not to pick one model strategy forever. The job is to create a platform path that can evolve across those strategies without rewriting every application each time.