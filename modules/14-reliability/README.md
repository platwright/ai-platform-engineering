# Module 14 - Reliability

## Overview

AI systems fail in ways that conventional SRE playbooks do not always anticipate. A model server can be healthy at the HTTP level while serving degraded outputs. A retrieval pipeline can succeed technically while returning stale documents. An agent can complete a tool loop while having made the wrong decision.

This module applies SRE-style reliability thinking to AI platform workloads. It covers failure taxonomy, SLI and SLO design, timeout and retry strategies, fallback patterns, backpressure, and incident response adapted for AI systems.

## Learning Objectives

By the end of this module, you should be able to:

- build a failure taxonomy for AI platform workloads covering both technical and quality failure modes
- define SLIs and SLOs that are meaningful for LLM serving, RAG, and agent systems
- design retry and timeout policies appropriate for stochastic AI workloads
- implement a fallback chain across model providers or serving paths
- apply backpressure and load shedding patterns to inference-heavy services
- write an incident response runbook for common AI platform failure scenarios
- declare and handle a quality incident where no HTTP error code is present

## Prerequisites

- Completion of [modules/13-ai-platform-security/README.md](../13-ai-platform-security/README.md)
- Familiarity with SRE fundamentals: error budgets, SLOs, toil
- Completion of Projects 01 through 04

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [Reliability for AI Workloads](chapters/01-reliability-for-ai-workloads.md)
2. [AI Platform Failure Taxonomy](chapters/02-ai-platform-failure-taxonomy.md)
3. [SLI and SLO Design for AI Systems](chapters/03-sli-and-slo-design.md)
4. [Timeouts and Retries](chapters/04-timeouts-and-retries.md)
5. [Fallback and Graceful Degradation](chapters/05-fallback-and-graceful-degradation.md)
6. [Backpressure and Load Shedding](chapters/06-backpressure-and-load-shedding.md)
7. [Disaster Recovery for AI Platforms](chapters/07-disaster-recovery.md)
8. [Incident Response for AI Platforms](chapters/08-incident-response.md)

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

- a documented failure taxonomy for the Acme AI platform
- defined SLOs for the sample-chat and sample-rag applications
- a working fallback simulation showing gateway provider switching
- a written incident response runbook for at least one failure mode

## Knowledge Check

1. Why does an HTTP 200 status code from a model server not confirm the system is working correctly?
2. What is the difference between a technical SLO (latency, availability) and a quality SLO (eval score)?
3. Why is exponential backoff with jitter preferred over fixed-interval retries for model API calls?
4. What is the difference between graceful degradation and fallback? Can a system use both?
5. Why can aggressive retries make a provider outage worse rather than better?
6. When should you use a circuit breaker for a model provider, and what state does it hold?
7. What is a "quality incident" and how do you declare one when there is no HTTP error?

## Common Mistakes

- measuring only HTTP success rate and ignoring quality degradation
- setting the same retry policy for transient errors and rate limit errors
- treating fallback as a reliability feature and not also testing that fallback itself can fail
- writing runbooks for infrastructure failures but not for quality failures
- setting SLOs without first establishing baselines from real traffic
- ignoring error budget burn rate until the budget is exhausted

## Production Considerations

- quality SLOs require evaluation infrastructure before they can be measured
- error budgets should gate change velocity: burning budget fast should slow down deployments
- fallback chains need their own observability so fallback use does not go unnoticed
- timeout values should be set based on measured p99 latency, not guesswork
- incident runbooks for AI platforms need AI-specific diagnostic steps, not just infrastructure steps

## Next Step

Read [concepts.md](concepts.md), then work through the SLO design and fallback exercises in [lab.md](lab.md).

## Overview

AI systems fail in ways that conventional SRE playbooks do not always anticipate. A model server can be healthy at the HTTP level while serving degraded or hallucinated outputs. A retrieval pipeline can succeed technically while returning stale, irrelevant, or incoherent documents. An agent can complete a tool loop successfully while having made the wrong decision.

This module applies SRE-style reliability thinking to AI platform workloads. It covers failure taxonomy, SLI and SLO design, timeout and retry strategies, fallback patterns, and incident response adapted for AI systems.

## Intended Learning Objectives

By the end of this module, learners should be able to:

- build a failure taxonomy for AI platform workloads covering both technical and quality failure modes
- define SLIs and SLOs that are meaningful for LLM serving, RAG, and agent systems
- design retry and timeout policies appropriate for stochastic AI workloads
- implement a fallback chain across model providers or serving paths
- apply backpressure and load shedding patterns to inference-heavy services
- write an incident response runbook for common AI platform failure scenarios

## Prerequisites

- Completion of Module 12 (Observability)
- Familiarity with SRE fundamentals (error budgets, SLOs, toil)
- Completion of Project 01 through Project 04

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Planned Chapter Structure

1. Reliability for AI Workloads
2. AI Platform Failure Taxonomy
3. SLI and SLO Design for AI Systems
4. Timeouts and Retries
5. Fallback and Graceful Degradation
6. Backpressure and Load Shedding
7. Disaster Recovery for AI Platforms
8. Incident Response for AI Platforms

## Planned Module Assets

- concepts.md
- architecture.md: failure taxonomy diagram for the Acme AI platform
- lab.md: deliberately trigger three failure modes and practice recovery using the failure labs
- challenge.md
- verification.md
- solution.md
- references.md

## Planned Lab Scope

The lab will:

1. Trigger a model provider timeout and observe how the gateway handles it
2. Trigger a retrieval failure and observe how the RAG pipeline degrades
3. Trigger an OOM event on the model serving container and practice recovery
4. Define an SLO for the sample-chat application and calculate its current error budget

## AI Platform Failure Taxonomy

| Category | Examples |
|---|---|
| Infrastructure failure | GPU OOM, container crash, node failure, network partition |
| Provider failure | Hosted API timeout, rate limit, 500 error, outage |
| Quality failure | Hallucination, wrong retrieval, incorrect tool call, broken output format |
| Configuration failure | Wrong model version, broken prompt, parameter misconfiguration |
| Data failure | Stale index, missing document, embedding mismatch, tenant boundary violation |
| Cascading failure | Retry storm, cache stampede, queue backup under load |

## SLO Design Guidance

AI system SLOs need to cover both technical and quality dimensions:

| SLI | Example SLO |
|---|---|
| Request success rate | 99.5% of chat requests complete without a 5xx response |
| TTFT | 95% of requests have TTFT < 800ms |
| End-to-end latency | 99% of requests complete within 8 seconds |
| Retrieval success | 99% of RAG queries return at least one relevant chunk |
| Tool execution success | 99.9% of approved tool calls complete without error |
| Quality score | Automated evaluation score stays above 0.80 on the standard evaluation set |

## Production Considerations This Module Will Address

- How do you set a TTFT SLO when model generation time is variable?
- What is the right retry policy for a model that occasionally returns malformed JSON?
- When should a fallback to a smaller model be triggered automatically versus manually?
- How do you declare a quality incident when there is no HTTP error code?

## Next Step

This module will be written in Phase 5. See [modules/15-scaling-and-performance/README.md](../15-scaling-and-performance/README.md) for the companion module.