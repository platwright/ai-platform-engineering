# Module 03 Concepts

## Why Application Architecture Matters

Before you deploy anything, you need to know what you are actually deploying. AI applications are not only "frontend plus model call." They usually include several internal layers with different failure modes, ownership boundaries, and scaling characteristics.

## The Common Request Path

An AI application often looks like this:

- frontend or calling client
- application API
- prompt and orchestration layer
- model access layer
- provider or model runtime

As capabilities grow, more pieces appear:

- retrieval
- tool execution
- safety checks
- caching
- sessions or conversation state
- evaluation and tracing hooks

## Application Layer vs Platform Layer

This module stays focused on the application layer, but the boundary matters.

Application teams usually own:

- product flows
- user experience
- business logic
- task-specific prompt behavior

Platform teams usually own reusable capabilities such as:

- model routing
- provider abstraction
- standard observability hooks
- shared auth patterns
- retrieval services
- policy controls

Project 01 sits near that boundary. It starts as application architecture, but it begins to look like a reusable platform component.

## State Is A Design Choice

AI applications often feel stateful because users have conversations, uploaded documents, tools, or memories. The key question is where the state lives.

Good architecture makes state explicit:

- session store
- cache
- vector store
- database
- queue

Hidden state inside application memory makes scaling and debugging harder.

## Synchronous And Asynchronous Are Product Decisions First

The workload shape usually starts with the user experience.

- chat is synchronous because the user waits for the answer
- indexing is asynchronous because the user should not wait for a long ingestion pipeline
- batch embeddings are asynchronous because throughput matters more than individual response latency

## Configuration Is Behavior

In AI systems, configuration can materially change outputs. Model selection, prompts, temperature, tool availability, and rate limits are not cosmetic settings. They are part of runtime behavior and should be treated with production discipline.

## Twelve-Factor Still Applies, But It Needs Translation

Cloud-native application discipline still matters. AI systems still benefit from clear config, explicit backing services, stateless processes, environment parity, and observable logs. The AI twist is that prompts, model choices, evaluations, and retrieval configuration now sit next to traditional app config.