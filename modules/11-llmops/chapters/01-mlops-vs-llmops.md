# Chapter 01 - MLOps vs LLMOps

## MLOps: The Foundation

MLOps is the practice of applying DevOps and software engineering discipline to machine learning workflows. It covers:

- **Training pipelines**: reproducible, versioned workflows that produce model artifacts
- **Model registries**: storing, versioning, and promoting model artifacts across environments
- **Feature stores**: managing the input features that models depend on
- **Deployment automation**: serving models in containers with health checks, scaling, and rollback
- **Monitoring**: data drift detection, prediction distribution tracking, performance degradation

MLOps brought rigor to a field that previously operated with a lot of notebook-driven, ad hoc processes. It is mature, well-tooled, and essential for organizations training their own models.

## What LLMOps Adds

LLMOps inherits all of MLOps and extends it to address the specific operational reality of large language models used through prompting rather than fine-tuning.

The key differences:

| Dimension | MLOps | LLMOps |
|---|---|---|
| Model artifact | Trained by you, stored internally | Mostly a vendor API or open-weight download |
| What you control | Model architecture, weights, training data | Prompts, configuration, retrieval pipeline |
| Evaluation output | Numeric score on a labeled test set | Open-ended text that needs rubric or LLM scoring |
| Determinism | Same input → same prediction | Same input → likely similar but different text |
| Regression signal | Accuracy drops below threshold | Quality degrades in ways hard to detect automatically |
| "Code" that changes behavior | Python model code | Prompt templates, system prompts, few-shot examples |
| Deployment artifact | Model container | Prompt version + model pin + config |

## The Shared Foundation

Despite the differences, LLMOps depends on the same foundational practices:

- **Version control**: every artifact that affects production behavior must be in version control
- **CI/CD**: every change should go through automated validation before reaching production
- **Monitoring**: every production system should produce telemetry that enables diagnosis
- **Rollback**: every deployment should be reversible
- **Review**: every change should have a defined review process

The challenge is applying these practices to artifacts — prompts, evaluation datasets, generation parameters — that development teams have historically not treated as serious engineering artifacts.

## Why This Matters For Platform Engineers

Platform engineers do not write the prompts. But they own the infrastructure that manages, evaluates, deploys, and monitors them. That means:

- the prompt registry is a platform service, like a container registry
- the evaluation runner is a platform capability, like a test runner
- the CI gate for AI changes is a platform integration point
- the rollback mechanism for prompts is a platform operational tool

Understanding where MLOps ends and LLMOps begins helps platform engineers know which problems are theirs to solve versus which are shared with application teams.

## Tooling Landscape Overview

| Category | MLOps Tools | LLMOps Extensions |
|---|---|---|
| Experiment tracking | MLflow, Weights & Biases | LangSmith, PromptLayer, Helicone |
| Model / prompt registry | MLflow Model Registry, BentoML | LangSmith, W&B Prompts, custom |
| Evaluation | Evidently, Great Expectations | RAGAS, DeepEval, Promptfoo |
| CI/CD | GitHub Actions, CircleCI | + eval steps in existing pipelines |
| Monitoring | Prometheus, Grafana | + LLM-specific exporters, OpenLLMetry |

The tool names will change. The capability categories will not.
