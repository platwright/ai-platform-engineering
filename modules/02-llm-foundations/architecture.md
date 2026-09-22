# Module 02 Architecture

## The LLM Request Path

```mermaid
flowchart LR
    App[Application] --> GW[AI Gateway]
    GW --> Model[LLM Endpoint]
    Model --> GW
    GW --> App

    subgraph "Request"
        Prompt[Prompt Tokens]
        Tools[Tool Definitions]
        Params[Generation Params]
    end

    subgraph "Response"
        Text[Text Content]
        ToolCall[Tool Calls]
        Usage[Token Usage]
    end
```

## Tokenization Flow

```mermaid
flowchart LR
    Text["Raw Text\n'Platform engineers build AI platforms.'"]
    Tokenizer["Tokenizer\n(BPE / WordPiece / SentencePiece)"]
    IDs["Token IDs\n[12107, 12604, 1382, 15068, 15108, 13]"]
    Embed["Token Embeddings\n(dense vectors)"]
    Model["Transformer\n(attention layers)"]

    Text --> Tokenizer --> IDs --> Embed --> Model
```

## Context Window Composition

```
┌─────────────────────────────────────────────────────────┐
│                   Context Window                        │
│  Max: 128,000 tokens                                    │
├──────────────────┬──────────────────┬───────────────────┤
│  System Prompt   │  Retrieved Docs  │  Conversation     │
│  ~600 tokens     │  ~2,000 tokens   │  History          │
│                  │                  │  ~500 tokens       │
├──────────────────┴──────────────────┴───────────────────┤
│  User Turn: ~100 tokens                                 │
├─────────────────────────────────────────────────────────┤
│  Output Reserve: ~500 tokens                            │
└─────────────────────────────────────────────────────────┘
```

## Tool Calling Loop

```mermaid
sequenceDiagram
    participant App as Application
    participant Model as LLM
    participant Tool as Tool Executor

    App->>Model: Request + Tool Definitions + User Message
    Model-->>App: tool_calls: [{name: "get_metrics", args: {...}}]
    App->>Tool: Execute get_metrics(...)
    Tool-->>App: {"latency_p99": 320, "error_rate": 0.008}
    App->>Model: Previous context + Tool Result
    Model-->>App: Final text response
```

## Streaming Response Path

```mermaid
sequenceDiagram
    participant Client
    participant Gateway
    participant Model as Model Server

    Client->>Gateway: POST /v1/chat/completions (stream: true)
    Gateway->>Model: Forward request
    Model-->>Gateway: SSE chunk: "data: {...token...}"
    Gateway-->>Client: Pass-through chunk (no buffer)
    Model-->>Gateway: SSE chunk: "data: {...token...}"
    Gateway-->>Client: Pass-through chunk
    Model-->>Gateway: data: [DONE]
    Gateway-->>Client: data: [DONE]
    Note over Gateway: Log complete response async
```

## Hosted vs Self-Hosted Decision Model

```mermaid
flowchart TD
    Start[New Model Use Case] --> Sensitive{Contains sensitive\nor regulated data?}
    Sensitive -- Yes --> SelfHost[Self-Hosted]
    Sensitive -- No --> Volume{High token\nvolume?}
    Volume -- Yes --> BreakEven{Self-host cheaper\nat this volume?}
    BreakEven -- Yes --> SelfHost
    BreakEven -- No --> Hybrid[Hybrid: route by\nload and sensitivity]
    Volume -- No --> Frontier{Needs frontier\ncapabilities?}
    Frontier -- Yes --> Hosted[Hosted API]
    Frontier -- No --> Hybrid
```
