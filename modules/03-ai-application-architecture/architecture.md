# Module 03 Architecture

## Core Request Path

```mermaid
flowchart LR
    User[User or Calling Service] --> Frontend[Frontend or Client]
    Frontend --> API[Application API]
    API --> Prompt[Prompt and Orchestration Layer]
    Prompt --> ModelClient[Unified Model Client]
    ModelClient --> Provider[Provider API or Model Runtime]
    Provider --> Response[Generated Response]
```

## Stateful Concerns Around The Request Path

```mermaid
flowchart TB
    API[Application API]
    Sessions[Session Store]
    Cache[Prompt or Response Cache]
    Vector[Vector Store]
    DB[Application Database]

    API --> Sessions
    API --> Cache
    API --> Vector
    API --> DB
```

## Synchronous And Asynchronous Split

```mermaid
flowchart LR
    UserReq[User Request] --> SyncAPI[Synchronous API Path]
    SyncAPI --> ModelClient[Unified Model Client]
    ModelClient --> Model[Model Provider]

    Documents[Documents or Batch Inputs] --> Queue[Queue or Job Trigger]
    Queue --> Worker[Asynchronous Worker]
    Worker --> Embed[Embedding or Batch Inference]
    Embed --> Storage[Database or Vector Store]
```

## Project 01 Application Shape

```mermaid
flowchart LR
    CLIorHTTP[CLI or Local HTTP API] --> App[Unified Model Client App]
    App --> PromptLayer[Prompt Layer]
    App --> Config[App Configuration]
    App --> Adapters[Provider Adapters]
    Adapters --> Mock[Mock Providers]
    Adapters --> Hosted[OpenAI-Compatible Provider]
```

## What To Notice

- the model call is only one part of the application
- prompt handling and provider transport should not be tightly coupled
- state should live in explicit services, not accidental process memory
- user-facing and background AI work should not share the same operational assumptions