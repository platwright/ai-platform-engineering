# Project 01 Architecture

## Application View

```mermaid
flowchart LR
    Caller[CLI or HTTP Caller] --> App[Project 01 App]
    App --> Prompt[Prompt Layer]
    App --> Config[Config Loader]
    App --> Client[Unified Model Client]
    Client --> Adapters[Provider Adapters]
    Adapters --> Mock[Mock Providers]
    Adapters --> Hosted[OpenAI-Compatible Provider]
```

## Local HTTP API View

```mermaid
flowchart LR
    User[Caller] --> API[/api/chat]
    API --> Service[UnifiedModelClient.chat]
    Service --> Provider[Selected Provider Adapter]
    Provider --> Result[Normalized Result]
    Result --> RunArtifact[Saved JSON Artifact]
```

## Internal Separation

```mermaid
flowchart TB
    Config[config.py]
    Service[service.py]
    Providers[providers.py]
    Server[server.py]

    Config --> Service
    Providers --> Service
    Service --> Server
```

## What To Notice

- config loading is separate from provider transport
- provider selection is explicit and named
- the same unified client can power both CLI and HTTP entry points
- mock providers make local validation easy before any real API key exists