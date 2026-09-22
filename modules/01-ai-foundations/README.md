# Module 01 - AI Foundations

## Overview

This module gives platform engineers the minimum AI mental model needed to make sensible infrastructure and platform decisions. It is intentionally practical. The goal is not to teach deep mathematics or model research. The goal is to explain what the workload is, how it behaves, and why platform choices change when AI enters the system.

The module ends with a small runnable project that measures an AI inference call like an operator would: latency, token usage, response content, and error behavior.

## Learning Objectives

By the end of this module, you should be able to:

- explain the relationship between AI, machine learning, deep learning, generative AI, foundation models, and LLMs
- distinguish clearly between training and inference workloads
- describe how parameters, precision, quantization, context windows, and tokens affect operational behavior
- compare proprietary, open-weight, hosted, self-hosted, and fine-tuned model strategies
- explain what embeddings are and why they matter to retrieval systems
- categorize common AI workload types and their infrastructure patterns
- map the AI lifecycle from experiment to production improvement
- run a mini-project that captures request latency, token usage, responses, and failures from an AI endpoint

## Prerequisites

- Completion of [modules/00-getting-started/README.md](../00-getting-started/README.md)
- A working Python installation
- Familiarity with basic command-line usage

## Difficulty And Time

- Difficulty: Beginner to intermediate
- Estimated time: 4 to 6 hours

## Module Map

### Chapters

1. [AI, ML, and Deep Learning](chapters/01-ai-ml-and-deep-learning.md)
2. [Training vs Inference](chapters/02-training-vs-inference.md)
3. [Models and Model Parameters](chapters/03-models-and-model-parameters.md)
4. [Foundation Models](chapters/04-foundation-models.md)
5. [Embeddings](chapters/05-embeddings.md)
6. [AI Workload Types](chapters/06-ai-workload-types.md)
7. [AI Lifecycle](chapters/07-ai-lifecycle.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)
- [Mini Project](project/README.md)

## Expected Outcome

At the end of this module, you should have:

- a concise mental model of common AI workloads
- a clear explanation of why training and inference produce different infrastructure requirements
- working vocabulary for model size, precision, tokens, context windows, embeddings, and workload types
- a run artifact from the mini-project showing latency, usage, output text, and error data
- notes in your workbook about which workload patterns look most relevant to your current role

## Knowledge Check

1. Why is a platform engineer more concerned with inference patterns than with training algorithms in most production organizations?
2. What operational difference exists between a model with many parameters and a model that merely has a long context window?
3. Why can embeddings become a platform concern even when no chatbot is involved?
4. What makes online inference operationally different from batch inference?
5. Why can a self-hosted open-weight model improve control while increasing operational burden?
6. Which lifecycle stages should produce artifacts that can be versioned and audited?

## Common Mistakes

- assuming AI is one workload type instead of several different operational patterns
- treating training and inference as the same resource problem
- using model size as the only signal of runtime cost or difficulty
- ignoring token usage and context windows when reasoning about cost and latency
- thinking embeddings are only relevant for search teams rather than for platform reuse

## Production Considerations

- model choice always affects cost, latency, privacy, and operational complexity
- inference paths need observability from the start, even in small prototypes
- hosted APIs simplify operations but create dependency, quota, and outage considerations
- response logging is useful, but prompts and outputs may contain sensitive data
- AI systems need lifecycle controls just like application code and infrastructure changes do

## Next Step

Read [concepts.md](concepts.md), then the chapters in order, then build the [mini project](project/README.md) through [lab.md](lab.md).