# Module 16 Concepts

## AI Costs Are Token-Level and Compound Quickly

Hosted API billing operates at the token level. A system that handles 1,000 requests per hour with 1,200 tokens per request processes 1.2 million tokens per hour. At $5 per million tokens, that is $6/hour or $4,380/month — from a workload that might feel small in HTTP request terms.

## Cost Visibility Requires Attribution

Cost that cannot be attributed to a team, product, or feature cannot be managed. Unattributed AI cost grows silently until it appears as a surprise on the monthly invoice. The first FinOps step is tagging every token to a tenant, product, or use case.

## Utilization Determines Effective Cost For Self-Hosted

A GPU instance that costs $4/hour and runs at 100% utilization has an effective per-inference cost of $4/hour of work. At 25% utilization, the same hardware produces 4× the cost per unit of work because 75% of the GPU hours are wasted. Self-hosted GPU cost management is fundamentally about utilization.

## Routing Decisions Are Financial Decisions

An AI gateway that routes all requests to a frontier model at $15/M output tokens makes a different financial decision than one that routes 80% to a smaller model at $0.60/M output tokens. Platform engineers who control the gateway control a significant fraction of the AI budget.

## Quality Must Be Preserved During Cost Optimization

Cost optimization that degrades response quality is not a net win. Shorter prompts save tokens but may reduce answer quality. Cheaper models have lower capability. Any cost optimization must be paired with an evaluation run to confirm quality is maintained above the SLO threshold.

## FinOps Is A Practice, Not A One-Time Project

AI costs evolve as traffic grows, new features are added, and model pricing changes. FinOps requires ongoing monitoring, periodic reviews, and continuous alignment between cost trends and budget expectations.
