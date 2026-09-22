# Module 16 - AI FinOps

## Overview

AI infrastructure costs can grow faster and more opaquely than conventional cloud workload costs. Token-level billing compounds quickly. GPU compute is expensive to waste. Model routing decisions directly affect monthly invoices. And without explicit cost attribution, engineering teams cannot tell which teams, applications, or features are driving spend.

This module applies FinOps practices to AI platform workloads, connecting platform design decisions to measurable cost behavior and giving teams the tools to observe, attribute, and control AI spending at scale.

## Learning Objectives

By the end of this module, you should be able to:

- calculate token-level cost for hosted API workloads at production volumes
- measure GPU utilization and identify waste in self-hosted deployments
- implement per-tenant cost attribution using gateway token usage data
- evaluate caching and routing decisions in cost terms with concrete numbers
- design environment-level cost controls for development and staging
- build a basic chargeback report for internal AI platform consumers
- explain the break-even analysis between hosted APIs and self-hosted infrastructure

## Prerequisites

- Completion of [modules/15-scaling-and-performance/README.md](../15-scaling-and-performance/README.md)
- Familiarity with basic cloud billing concepts
- Completion of Projects 01 through 04

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 5 to 7 hours

## Module Map

### Chapters

1. [AI Cost Visibility](chapters/01-ai-cost-visibility.md)
2. [Token Cost Modeling for Hosted APIs](chapters/02-token-cost-modeling.md)
3. [GPU Utilization and Self-Hosted Cost](chapters/03-gpu-utilization-and-self-hosted-cost.md)
4. [Cost Attribution and Tagging](chapters/04-cost-attribution-and-tagging.md)
5. [Caching and Routing as Cost Controls](chapters/05-caching-and-routing-as-cost-controls.md)
6. [Model Selection and Cost Tradeoffs](chapters/06-model-selection-and-cost-tradeoffs.md)
7. [Environment Cost Controls](chapters/07-environment-cost-controls.md)
8. [Chargeback and Usage Tracking](chapters/08-chargeback-and-usage-tracking.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Expected Outcome

At the end of this module, you should have:

- a working cost report script that reads gateway usage logs and calculates per-tenant costs
- a break-even analysis comparing hosted API cost vs self-hosted GPU cost for a hypothetical workload
- a designed chargeback model for the Acme AI platform
- notes on which cost optimization levers have the highest impact for your context

## Knowledge Check

1. A team sends 10 million input tokens and 2 million output tokens per day using a model priced at $5/M input and $15/M output. What is the daily and monthly cost?
2. A GPU server costs $2.50/hour. At 40% utilization, what is the effective cost per inference hour?
3. Why does routing 80% of requests to a cheap small model save more than 80% of the total cost?
4. What is the break-even point for switching from a hosted API to self-hosted GPU? What factors move it?
5. Why should dev and staging environments have separate cost controls from production?
6. What is the difference between showback and chargeback? Which is easier to start with?
7. Why does caching the same prompt repeatedly have diminishing returns on cost savings?

## Common Mistakes

- optimizing token usage without measuring the quality impact of shorter prompts
- attributing all AI cost to the model API and ignoring embedding service, vector DB, and infrastructure costs
- setting environment cost controls in production instead of dev/staging
- building a chargeback model before establishing cost visibility (need to measure before billing)
- over-investing in semantic caching when prompt cache hit rate is already high
- comparing hosted API cost to self-hosted cost without including the engineering cost of operating GPU infrastructure

## Production Considerations

- cost anomaly detection is as important as cost attribution: catch runaway spend before it appears on the monthly invoice
- model routing decisions that change production behavior need evaluation as well as cost analysis
- GPU utilization targets should balance cost efficiency against response latency (100% utilization typically means queuing)
- chargeback models create incentives — ensure the incentives are aligned with platform goals (quality, security, sustainability)

## Next Step

Read [concepts.md](concepts.md), then build the cost report in [lab.md](lab.md).

## Overview

AI infrastructure costs can grow faster and more opaquely than conventional cloud workload costs. Token-level billing compounds quickly. GPU compute is expensive to waste. Model routing decisions directly affect monthly invoices. And without explicit attribution, engineering teams cannot tell which teams, applications, or features are driving cost.

This module applies FinOps practices to AI platform workloads. It connects platform design decisions to measurable cost behavior and gives teams the tools to observe, attribute, and control AI spending at a sustainable scale.

## Intended Learning Objectives

By the end of this module, learners should be able to:

- calculate token-level cost for hosted API workloads at production volumes
- measure GPU utilization and identify waste in self-hosted deployments
- implement cost attribution for multi-tenant AI platform usage
- evaluate caching, routing, and model selection decisions in cost terms
- design environment-level cost controls for development and staging
- build a basic chargeback model for internal AI platform consumers

## Prerequisites

- Completion of Module 12 (Observability)
- Familiarity with cloud billing concepts
- Completion of Project 01 through Project 04

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 5 to 7 hours

## Planned Chapter Structure

1. AI Cost Visibility
2. Token Cost Modeling for Hosted APIs
3. GPU Utilization and Self-Hosted Cost
4. Cost Attribution and Tagging
5. Caching and Routing as Cost Controls
6. Model Selection and Cost Tradeoffs
7. Environment Cost Controls
8. Chargeback and Usage Tracking

## Planned Module Assets

- concepts.md
- architecture.md: cost attribution architecture across the AI gateway and platform layers
- lab.md: build a cost report from gateway token usage logs and compare routing scenarios
- challenge.md
- verification.md
- solution.md
- references.md

## Planned Lab Scope

The lab will:

1. Aggregate token usage from AI gateway request logs
2. Apply per-token pricing for two model tiers and calculate monthly projected cost
3. Simulate a caching scenario and calculate cost reduction
4. Design a simple per-tenant chargeback report

## Cost Modeling Framework

### Hosted API Cost

```
monthly_cost = 
    (monthly_input_tokens  / 1_000_000) × input_price_per_M  +
    (monthly_output_tokens / 1_000_000) × output_price_per_M
```

### Self-Hosted GPU Cost

```
monthly_cost = 
    gpu_instance_hours × hourly_rate ×
    (1 / gpu_utilization_fraction)
```

A GPU at 25% utilization has 4× the effective per-inference cost of a GPU at 100% utilization.

### Model Routing Cost Impact

Routing 80% of requests to a cheap small model and 20% to a frontier model can reduce costs by 60-80% compared to routing everything to the frontier model, if the quality trade-off is acceptable.

## Key Cost Signals

| Signal | What It Enables |
|---|---|
| prompt_tokens per request | Budget tracking, per-prompt cost attribution |
| completion_tokens per request | Output cost attribution |
| cost_per_session | Product-level cost visibility |
| cache_hit_rate | Quantify caching cost savings |
| gpu_utilization | Identify self-hosted waste |
| cost_by_tenant | Chargeback reporting |
| cost_by_model | Model tier cost comparison |

## Production Considerations This Module Will Address

- How do you set cost alerts before a billing surprise appears on the monthly invoice?
- What is the right granularity for cost attribution in a multi-tenant AI platform?
- How do you evaluate whether a caching investment pays for itself?
- What is the break-even analysis for switching a workload from a hosted API to self-hosted GPU?

## Next Step

This module will be written in Phase 5. See [modules/17-developer-platform/README.md](../17-developer-platform/README.md) for the companion module.