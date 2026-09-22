# Module 03 Challenge

## Challenge Prompt

Acme AI has three product teams:

- one wants a synchronous chat assistant
- one wants asynchronous document indexing and retrieval
- one wants both chat and tool-calling workflows

Design a shared application architecture approach that gives each team a stable interface without forcing all teams into the same state model or provider choice.

## Deliverable

Create a design note in:

- `my-solutions/module-03-ai-application-architecture.md`

Include:

1. which layers should be shared across teams
2. which layers remain application-specific
3. which state stores are explicit and why
4. which workloads are synchronous versus asynchronous
5. which configuration should be centrally managed

## Project 01 Extension

Propose how you would extend Project 01 to support:

- retries with policy
- a second prompt variant by configuration
- an asynchronous batch mode for document summarization
- usage tracking per team or application

## What Good Looks Like

A strong answer makes the state boundaries explicit, separates app logic from provider logic, and treats configuration and prompts as first-class artifacts rather than hidden constants.