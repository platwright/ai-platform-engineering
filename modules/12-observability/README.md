# Module 12 - Observability

## Overview

Observability for AI systems extends beyond conventional metrics, logs, and traces. The signals that matter are different: token usage, TTFT, generation rate, retrieval hit quality, tool call success rates, cost per session, and evaluation score trends sit alongside standard HTTP metrics, error rates, and latency distributions.

This module builds on the observability assets in the platform and extends them to cover the AI-specific signals that Acme AI needs to operate reliably. A platform that passes all HTTP health checks can still be generating poor-quality responses. Observability must cover both dimensions.

## Learning Objectives

By the end of this module, you should be able to:

- describe the four observability layers for AI systems: metrics, logs, traces, and evaluations
- instrument an AI application endpoint with LLM-specific OpenTelemetry span attributes
- define meaningful metrics for model serving, RAG, agent, and gateway layers
- build a Grafana dashboard that provides operational visibility into the AI platform
- design alert conditions for AI-specific failure modes including TTFT regression and cost spikes
- explain what evaluation-driven observability adds beyond runtime telemetry
- reason about privacy tradeoffs when logging prompt and response content

## Prerequisites

- Completion of [modules/11-llmops/README.md](../11-llmops/README.md)
- Familiarity with Prometheus metrics and Grafana dashboards at a basic level
- Completion of Projects 01 through 04

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [Observability Layers for AI Systems](chapters/01-observability-layers-for-ai-systems.md)
2. [Metrics and Telemetry for LLM Workloads](chapters/02-metrics-and-telemetry-for-llm-workloads.md)
3. [Distributed Tracing with LLM Context](chapters/03-distributed-tracing-with-llm-context.md)
4. [RAG Observability](chapters/04-rag-observability.md)
5. [Agent Observability](chapters/05-agent-observability.md)
6. [Gateway and Routing Observability](chapters/06-gateway-and-routing-observability.md)
7. [Dashboards and Alerting](chapters/07-dashboards-and-alerting.md)
8. [Evaluation-Driven Observability](chapters/08-evaluation-driven-observability.md)

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

- a clear understanding of which metrics matter most at each layer of the AI platform
- an instrumented endpoint producing token usage and latency measurements
- notes on a minimal dashboard design for the Acme AI platform
- a set of alert conditions suitable for an on-call runbook

## Knowledge Check

1. Why is a green HTTP health check not sufficient to confirm an AI system is working correctly?
2. What is the difference between TTFT and end-to-end latency, and why do you need both?
3. Name three signals that belong in RAG observability but not in generic HTTP service observability.
4. How do you trace a single user request across gateway, model serving, and RAG layers without creating a single monolithic span?
5. What privacy risk arises from logging full prompt and response content, and how do you mitigate it?
6. Why is a dashboard showing only request rate and error rate insufficient for AI platform operations?
7. What does "evaluation-driven observability" add that runtime telemetry cannot provide?

## Common Mistakes

- assuming that HTTP success rate and latency are sufficient observability for AI workloads
- logging raw prompt and response content without PII scrubbing or access controls
- using a single latency metric that conflates TTFT with generation time
- monitoring GPU utilization without also monitoring queue depth and KV cache pressure
- creating dashboards that are too dense to read during an incident
- alerting on every metric without a clear runbook for each alert condition

## Production Considerations

- token usage and cost metrics should flow to a FinOps dashboard alongside the ops dashboard
- traces for AI workloads can be expensive at full sampling; use head-based sampling with tail-based promotion for slow requests
- evaluation score trends belong on the platform dashboard alongside latency and error rate
- alert thresholds for AI systems need burn-rate logic (SLO-based alerting) rather than fixed-level thresholds
- on-call runbooks for AI systems need AI-specific diagnostic steps

## Next Step

Read [concepts.md](concepts.md), then instrument the sample-rag path in [lab.md](lab.md).