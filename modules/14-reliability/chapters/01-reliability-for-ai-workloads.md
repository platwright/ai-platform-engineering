# Chapter 01 - Reliability for AI Workloads

## Why AI Reliability Is Different

Conventional SRE reliability engineering is well-understood: define SLIs, set SLOs, maintain an error budget, automate deployment and rollback, write runbooks. These practices work well for systems where a correct response is deterministic and failure is binary.

AI workloads add a dimension that conventional reliability engineering was not designed for: **stochastic output quality**. The system can respond successfully at the HTTP level while producing responses that are incorrect, irrelevant, or harmful. Uptime is necessary but not sufficient.

## The Two Reliability Dimensions

Every AI platform SLO framework must cover both:

### Dimension 1: Technical Reliability

Standard SRE concerns:

- **Availability**: what fraction of requests complete without a 5xx error?
- **Latency**: what is the distribution of response times?
- **Error rate**: what fraction of requests fail for identifiable technical reasons?
- **Throughput**: can the system handle the expected request volume?

These are well-understood, well-tooled, and should be the starting point.

### Dimension 2: Quality Reliability

AI-specific concerns:

- **Groundedness**: are responses grounded in retrieved facts rather than fabricated?
- **Relevance**: do responses address the question asked?
- **Completeness**: do responses cover the required aspects?
- **Behavioral consistency**: does the model behave the same way given the same context?

Quality failures are harder to detect, harder to alert on, and harder to recover from because they do not produce error codes. They require evaluation pipelines (Module 11) to measure.

## The SRE Mindset Applied To AI

The SRE mindset — "reliability is a feature, not a property" — applies directly to AI systems with extensions:

| SRE Principle | AI Extension |
|---|---|
| Error budgets gate change velocity | Quality score budgets should also gate change velocity |
| Automate toil | Automate evaluation runs, fallback switches, and response validation |
| Blameless post-mortems | Include quality incidents in post-mortems, not just outages |
| Define SLOs from user perspective | User-perceived quality is as important as user-perceived latency |
| Runbooks enable consistent incident response | AI runbooks must include quality diagnostic steps |

## What Makes AI Failures Operationally Hard

### Failures Are Often Silent

A hallucinated response does not produce a log error. A stale RAG index does not cause a 500. An agent that made a poor tool call returns HTTP 200. Operators who rely only on error rates will miss most quality failures.

### Failures Are Context-Dependent

The same model prompt that works well for most inputs may fail for specific topics, writing styles, or question formulations. Evaluating only the happy path misses the long tail of real user behavior.

### Recovery Is Not Always Clear

For a crashed container, the recovery is: restart the container. For a model that has started producing lower-quality outputs due to a provider model update, the recovery options are: revert to the previous model version (if pinned), implement a workaround in the prompt, or accept the behavior change and update the SLO baseline. None of these are simple.

## Establishing Reliability Baselines

Before any SLO is meaningful, you need a baseline measured from real traffic:

1. Run the platform for at least one week with observability enabled
2. Measure p50, p95, p99 latency for each SLI
3. Measure error rate by error category
4. Run the evaluation suite to establish quality baseline
5. Record all of these as the foundation for SLO setting

Setting an SLO without a baseline leads to SLOs that are either too easy (no operational value) or too strict (constant alert noise and error budget burns before any real incident).
