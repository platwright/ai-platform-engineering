# Chapter 1.1 - AI, ML, and Deep Learning

## Why This Distinction Matters

Platform engineers do not need every research detail, but they do need precise vocabulary. Loose language creates bad system design. If every workload is called "AI," you lose the differences that matter for compute, latency, and operations.

## Artificial Intelligence

Artificial intelligence is the broadest category. It includes any system that performs tasks commonly associated with human intelligence, such as reasoning, language understanding, perception, planning, or decision-making.

Not every AI system is trained the same way, and not every AI system uses neural networks.

## Machine Learning

Machine learning is a subset of AI where systems learn patterns from data instead of being programmed only through explicit rules.

Examples:

- spam classification
- fraud detection
- recommendation systems
- demand forecasting

Many important platform lessons from ML still apply in generative AI environments, especially around lifecycle, evaluation, deployment, and monitoring.

## Deep Learning

Deep learning is a subset of machine learning built around neural networks with multiple layers. Modern image models, speech systems, and LLMs come from this area.

For platform engineers, deep learning usually matters because it changes:

- hardware expectations
- model artifact size
- memory pressure
- serving patterns
- batch and throughput behavior

## Generative AI

Generative AI produces new outputs rather than only classifying existing inputs. Outputs can include:

- text
- code
- images
- audio
- video

This matters operationally because the output length is variable and the system may hold long-lived requests open while generating tokens.

## Foundation Models

Foundation models are large pre-trained models that can support many downstream tasks. They are not limited to one single application. A team can prompt or fine-tune the same base model for multiple use cases.

That reusability is exactly why platform teams care. A shared platform becomes valuable only when several workloads can sit on top of the same model access, observability, and policy layers.

## LLMs

LLMs are foundation models focused on language. They can power chat, summarization, question answering, extraction, classification, tool calling, and code assistance.

They are central to this course because they introduce operational concerns that ordinary stateless APIs do not have:

- token accounting
- context windows
- streaming responses
- prompt artifacts
- retrieval augmentation
- model routing and fallback

## Common Misunderstandings

- AI does not always mean LLMs.
- ML does not always require GPUs.
- a bigger model does not automatically produce a better production outcome.
- a generative system may still depend on deterministic application controls around it.

## What The Platform Engineer Should Retain

The most important takeaway is not taxonomy for its own sake. It is that different AI subdomains imply different workload shapes, and different workload shapes imply different platform responsibilities.