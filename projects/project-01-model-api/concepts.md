# Project 01 Concepts

## Stable Interface First

The project starts from one core idea: the application should depend on a stable model client interface, not on a provider-specific response schema.

## Provider Adapters

Each provider can differ in:

- authentication
- endpoint URL
- request payload details
- response schema
- error behavior

Provider adapters isolate those differences so the application-facing interface stays stable.

## Prompt Layer

The project loads prompt artifacts from files instead of burying them inside transport code. That separation makes prompt changes more reviewable and easier to version.

## Config-Driven Behavior

The application chooses:

- default provider
- provider aliases
- prompt files
- generation defaults

through configuration. That means you can change behavior without rewriting the request path.

## Normalized Responses

The output shape is normalized across providers so application code can reason about:

- status
- latency
- token usage
- model name
- response text
- errors

without learning every provider's native payload.