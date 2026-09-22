# Module 11 - LLMOps

## Overview

LLMOps extends MLOps practices to the reality of language model production systems. Where MLOps focuses on training pipelines and model registries, LLMOps adds the concerns specific to generative AI: prompts as versioned artifacts, evaluation against open-ended outputs, regression detection for non-deterministic systems, and the operational integration of human feedback loops.

This module grounds LLMOps in the Acme AI narrative. Acme needs to know when a prompt change causes a regression, whether a new model version produces better or worse results on real traffic, and how to release changes with enough confidence to avoid production incidents.

## Learning Objectives

By the end of this module, you should be able to:

- distinguish MLOps and LLMOps and explain which practices apply to both
- describe prompt versioning, storage, and promotion as production engineering concerns
- design evaluation datasets that test meaningful platform behaviors
- build a basic automated evaluation loop for a RAG system
- explain regression testing strategies for non-deterministic model outputs
- describe how an AI CI/CD pipeline differs from a standard application pipeline
- identify LLMOps tooling categories and when each matters

## Prerequisites

- Completion of [modules/10-agent-platform/README.md](../10-agent-platform/README.md)
- Familiarity with CI/CD concepts and basic pipeline tooling
- Completion of Projects 01 through 04

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [MLOps vs LLMOps](chapters/01-mlops-vs-llmops.md)
2. [Versioning Prompts, Models, and Config](chapters/02-versioning-prompts-models-and-config.md)
3. [Prompt Registries and Management](chapters/03-prompt-registries-and-management.md)
4. [Evaluation Dataset Design](chapters/04-evaluation-dataset-design.md)
5. [Automated Evaluation Patterns](chapters/05-automated-evaluation-patterns.md)
6. [Regression Detection](chapters/06-regression-detection.md)
7. [AI CI/CD Pipelines](chapters/07-ai-cicd-pipelines.md)
8. [Human Feedback Integration](chapters/08-human-feedback-integration.md)

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

- a clear mental model of how LLMOps extends and differs from MLOps
- a working evaluation script that scores RAG responses against a test dataset
- a prompt versioning and promotion workflow described in your workbook
- notes on what CI gates and regression thresholds are appropriate for the Acme AI platform

## Knowledge Check

1. Why does non-determinism make conventional exact-match testing insufficient for LLM outputs?
2. What information should a prompt version record track beyond the prompt text itself?
3. What is the difference between an evaluation dataset and a benchmark? When does each apply?
4. Why is LLM-as-judge evaluation useful, and what are its reliability limits?
5. Which changes to an AI system should trigger a full evaluation run versus a lightweight smoke test?
6. What does "silent model drift" mean and how would you detect it?
7. How is deploying a new prompt version different from deploying new application code?

## Common Mistakes

- treating prompts as immutable strings in source code instead of versioned operational artifacts
- running evals only on happy-path inputs and missing real-world edge cases
- using exact match scoring for open-ended generation tasks
- blocking every CI run on expensive full evaluation suites instead of tiering eval costs
- collecting human feedback without a plan to close the loop back to the model or prompt

## Production Considerations

- prompt changes should be deployed with the same review and rollback capabilities as code changes
- evaluation score baselines must be established before any regression alerting makes sense
- eval datasets need maintenance: stale test cases produce misleading pass rates
- human feedback is a sampling signal, not ground truth — treat it statistically
- CI eval runs should produce artifacts that humans can audit, not just pass/fail status

## Next Step

Read [concepts.md](concepts.md), then work through the chapters in order before building the evaluation loop in [lab.md](lab.md).