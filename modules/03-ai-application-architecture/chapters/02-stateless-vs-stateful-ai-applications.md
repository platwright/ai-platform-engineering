# Chapter 3.2 - Stateless vs Stateful AI Applications

## Why This Distinction Matters

Statelessness is still one of the simplest ways to scale application processes, but AI products often introduce pressure toward state: conversations, memory, document context, cached results, and user sessions.

The goal is not to eliminate state. The goal is to place state deliberately.

## Stateless AI Applications

A stateless application process does not rely on in-memory process state from previous requests to function correctly.

Examples:

- one-shot classification
- summarization of a single input payload
- extraction from a single document passed in the request

Benefits:

- easier horizontal scaling
- simpler rollouts
- lower coupling between requests

## Stateful AI Applications

A stateful AI application depends on information beyond the current request.

Examples:

- conversation history
- user preferences
- long-running agent tasks
- retrieval indexes
- workflow checkpoints

State is not bad, but invisible state is bad.

## Common State Locations

- session stores for conversation context
- caches for prompt or response reuse
- databases for workflow or user records
- vector stores for retrieval context
- object storage for uploaded artifacts

## Hidden State Problems

Hidden state often appears as:

- in-memory conversation history inside one application process
- environment-specific prompt files no one tracks
- local caches with no invalidation strategy

That breaks scaling, debugging, and reproducibility.

## Design Guidance

Prefer this question over "Is the app stateful?"

Ask instead:

- what state exists?
- who owns it?
- where does it live?
- what is its lifecycle?
- how is it protected?
- how is it observed?

## Platform Takeaway

Scaling AI applications is easier when the application process is as stateless as practical and any required state is explicit, externalized, and governed.