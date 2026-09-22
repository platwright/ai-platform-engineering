# Module 02 - LLM Foundations

## Overview

This module explains how large language model inference works from a platform engineering perspective. It does not teach model training or machine learning theory. It teaches the runtime behavior, protocols, and tradeoffs that directly affect infrastructure, cost, latency, and platform design decisions.

Platform engineers who understand tokenization, context windows, generation parameters, structured outputs, tool calling, and streaming can make defensible decisions about serving, monitoring, routing, and cost control. Platform engineers who do not will be guessing.

## Learning Objectives

By the end of this module, you should be able to:

- explain how tokenization maps text to tokens and why token counts drive cost and capacity decisions
- describe context windows and their operational implications for memory and request handling
- configure and reason about generation parameters including temperature, top-p, and max tokens
- explain what structured output modes provide and where they break down
- describe the tool calling protocol as a platform surface with authorization and auditability requirements
- compare streaming and non-streaming response paths and their infrastructure implications
- make informed initial decisions about hosted versus self-hosted model access

## Prerequisites

- Completion of [modules/01-ai-foundations/README.md](../01-ai-foundations/README.md)
- Familiarity with HTTP APIs and JSON
- A working Python environment

## Difficulty And Time

- Difficulty: Beginner to intermediate
- Estimated time: 4 to 6 hours

## Module Map

### Chapters

1. [Tokenization and Context Windows](chapters/01-tokenization-and-context-windows.md)
2. [Generation Parameters](chapters/02-generation-parameters.md)
3. [Structured Outputs](chapters/03-structured-outputs.md)
4. [Tool Calling](chapters/04-tool-calling.md)
5. [Streaming](chapters/05-streaming.md)
6. [Hosted vs Self-Hosted Models](chapters/06-hosted-vs-self-hosted.md)

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

- a clear mental model of how LLM inference works at the request level
- the vocabulary to reason about cost, latency, and capacity in terms of tokens
- confidence in reading and configuring generation parameter settings
- an understanding of why tool calling and structured output are platform surfaces rather than just model features
- notes in your workbook about which aspects of LLM behavior you will need to monitor and govern

## Knowledge Check

1. Why does a 2,000-token system prompt cost more to run than a 200-token system prompt, even if the user message is the same length?
2. What is the operational difference between a 4K context window model and a 128K context window model beyond the obvious size difference?
3. What does `temperature=0` actually mean, and why is it not truly deterministic?
4. When would you use `response_format: json_object` versus a schema-constrained structured output? What does each guarantee?
5. Why is tool calling a platform security concern, not just a model feature?
6. Why might you choose a self-hosted 70B model over a hosted frontier model for a high-volume internal use case?
7. What does TTFT measure and why is it the metric most users implicitly care about?

## Common Mistakes

- treating token count as roughly equivalent to word count without verifying for the actual model tokenizer
- setting no `max_tokens` limit and assuming the model will always stop naturally
- relying on JSON mode alone for structured output parsing without schema validation
- treating tool definitions as static strings instead of versioned, governed contracts
- deploying streaming without verifying that the gateway and load balancer support long-lived chunked connections
- assuming all open-weight models are freely usable commercially without reading their licenses

## Production Considerations

- every model request should log token usage — unexplained growth is often the first signal of a prompt regression
- generation parameter defaults should be documented and version-controlled alongside prompt assets
- structured output schemas are API contracts: breaking changes need backward-compatible migration paths
- tool schemas need authorization policies before any destructive or side-effecting tools are exposed
- TTFT targets should be defined early and influence model and serving choices
- the hosted vs self-hosted decision should be revisited periodically as token volumes, model capabilities, and GPU economics change

## Next Step

Read [concepts.md](concepts.md), then work through the chapters in order before completing [lab.md](lab.md).