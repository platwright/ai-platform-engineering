# Chapter 3.1 - Anatomy of an AI Application

## The Basic Shape

An AI application often starts with a user experience and ends with a model response, but several layers sit between those two points.

```text
Frontend
  -> Application API
  -> Prompt layer
  -> AI gateway or model client
  -> Model provider or model runtime
```

That layered view matters because each layer has different responsibilities and different failure modes.

## Frontend Or Calling Client

This is the user-facing or service-facing surface:

- web UI
- CLI
- internal API consumer
- workflow engine

Its job is usually to collect intent and present results, not to know the details of model provider APIs.

## Application API

The application API translates a user action into an application-specific request. It should own:

- request validation
- auth context propagation
- business constraints
- response shaping for the caller

It should not become a dumping ground for model-provider-specific logic.

## Prompt Layer

The prompt layer decides how the task is framed for the model. This can include:

- system prompts
- prompt templates
- retrieved context
- tool availability
- output formatting instructions

Treating prompt construction as a visible layer makes behavior easier to test, review, and change.

## Model Access Layer

This is where provider-specific transport details belong. In small systems it may be a client library or adapter. In larger systems it can evolve into a gateway or shared platform API.

The key idea is stability: application code should not need to rewrite itself every time a provider, model, or auth method changes.

## Backing Services Around The Request

Many AI applications also depend on:

- session stores
- caches
- vector stores
- databases
- queues

Those are architectural choices, not incidental details.

## Platform Takeaway

The anatomy matters because later platform work depends on it. If the application mixes prompt logic, provider transport, state, and business rules in one place, every later operational task becomes harder.