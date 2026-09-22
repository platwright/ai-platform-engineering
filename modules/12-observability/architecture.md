# Module 12 Architecture

## AI Platform Observability Stack

```mermaid
flowchart TB
    App[Application\nSample Chat/RAG/Agent]
    GW[AI Gateway]
    Model[Model Server\nvLLM]
    RAG[RAG Platform\nProject 03]
    Agent[Agent Platform\nProject 04]

    OTel[OpenTelemetry Collector]
    Prom[Prometheus]
    Jaeger[Jaeger\nDistributed Tracing]
    Grafana[Grafana\nDashboards + Alerts]

    App --> OTel
    GW --> OTel
    Model --> OTel
    RAG --> OTel
    Agent --> OTel

    OTel --> Prom
    OTel --> Jaeger

    Prom --> Grafana
    Jaeger --> Grafana
```

## Distributed Trace: RAG Request

```mermaid
sequenceDiagram
    participant Client
    participant App as Application\n(span: app.chat_request)
    participant GW as AI Gateway\n(span: gateway.route)
    participant Embed as Embedding\n(span: rag.embed_query)
    participant VDB as Vector DB\n(span: rag.retrieve)
    participant Rerank as Reranker\n(span: rag.rerank)
    participant LLM as Model Server\n(span: llm.generate)

    Client->>App: POST /api/chat
    App->>GW: POST /api/chat (trace-id propagated)
    GW->>Embed: embed(question)
    Embed-->>GW: vector
    GW->>VDB: search(vector, top_k=10)
    VDB-->>GW: chunks[]
    GW->>Rerank: rerank(question, chunks)
    Rerank-->>GW: ranked_chunks[]
    GW->>LLM: chat(system+context, question)
    LLM-->>GW: response + usage
    GW-->>App: response
    App-->>Client: response
```

## Metric Layers

```mermaid
flowchart LR
    subgraph "Infrastructure"
        GPU[GPU utilization\nmemory\ntemperature]
        CPU[CPU / mem\nnode health]
    end

    subgraph "Model Serving"
        TTFT[time_to_first_token]
        TPS[tokens_per_second]
        Queue[queue_depth]
        KV[kv_cache_utilization]
    end

    subgraph "AI Gateway"
        Req[request_rate\nerror_rate]
        Route[route_selected\nfallback_events]
        Tokens[prompt_tokens\ncompletion_tokens]
        Cost[cost_rate_per_tenant]
    end

    subgraph "RAG"
        Ingest[ingestion_success\nchunks_per_doc]
        Retrieval[retrieval_latency\nhit_count]
        Freshness[index_age_hours]
    end

    subgraph "Quality"
        EvalScore[eval_score_trend]
        Feedback[negative_feedback_rate]
    end
```

## Dashboard Layout

```
┌──────────────────────────────────────────────────────────────────┐
│ Platform Overview                          [time range: 1h / 6h] │
├──────────┬──────────┬──────────┬──────────┬──────────────────────┤
│ Req/min  │ Error %  │ TTFT p50 │ TTFT p95 │  Cost/hr (tokens)   │
│   432    │  0.8%    │  380ms   │  980ms   │     $0.42           │
├──────────┴──────────┴──────────┴──────────┴──────────────────────┤
│ Request Rate (by model)          │ Token Usage (by tenant)        │
│ [time series]                    │ [stacked bar]                  │
├──────────────────────────────────┤────────────────────────────────┤
│ TTFT Distribution (heatmap)      │ RAG Retrieval Latency          │
├──────────────────────────────────┤────────────────────────────────┤
│ GPU Utilization (by node)        │ Eval Score (7-day trend)       │
└──────────────────────────────────┴────────────────────────────────┘
```
