# Chapter 04 - RAG Observability

## Why RAG Needs Its Own Observability

A RAG system is not a single service. It is a pipeline: document ingestion → chunking → embedding → storage → query embedding → vector search → reranking → grounded generation. Each stage can fail or degrade independently. A generic HTTP monitor watching the query endpoint only tells you whether the endpoint responds — it says nothing about retrieval quality, index freshness, or embedding accuracy.

## Ingestion Pipeline Signals

The ingestion pipeline runs as a background or batch job. Its health signals are separate from query-time signals.

| Signal | Type | Description |
|---|---|---|
| `rag_ingestion_documents_total` | Counter | Documents ingested by tenant |
| `rag_ingestion_chunks_total` | Counter | Chunks produced per ingestion job |
| `rag_ingestion_errors_total` | Counter | Parsing or embedding failures |
| `rag_ingestion_duration_seconds` | Histogram | Time to ingest a batch |
| `rag_index_last_updated_timestamp` | Gauge | Epoch timestamp of most recent successful ingest |
| `rag_index_document_count` | Gauge | Current document count by tenant |
| `rag_index_chunk_count` | Gauge | Current chunk count by tenant |

The `rag_index_last_updated_timestamp` is the most important operational signal for freshness. Alert when this timestamp is older than the acceptable staleness window.

```promql
# Alert when index is more than 24 hours old
(time() - rag_index_last_updated_timestamp) > 86400
```

## Query-Time Signals

| Signal | Type | Description |
|---|---|---|
| `rag_query_total` | Counter | Queries by tenant and status |
| `rag_query_duration_seconds` | Histogram | End-to-end query latency |
| `rag_embed_duration_seconds` | Histogram | Query embedding latency |
| `rag_vector_search_duration_seconds` | Histogram | Vector search latency |
| `rag_rerank_duration_seconds` | Histogram | Reranker latency |
| `rag_chunks_retrieved_count` | Histogram | Distribution of retrieved chunk counts |
| `rag_chunks_after_rerank_count` | Histogram | Distribution after reranking |
| `rag_zero_result_queries_total` | Counter | Queries that returned no chunks |

Zero-result queries are a critical signal. They indicate that the query had no overlap with the indexed content, which may indicate:
- the question is genuinely out of scope
- the index is stale or missing relevant documents
- the query embedding is failing
- the similarity threshold is too high

## Latency Decomposition For RAG

The total RAG query latency decomposes across:

```
total = embed_query + vector_search + rerank + llm_generate

Example:
  embed_query:    45ms
  vector_search:  18ms
  rerank:         120ms
  llm_generate:   1,650ms
  ─────────────────────
  total:          1,833ms
```

The LLM generation step usually dominates. But if reranking starts taking 500ms instead of 120ms, the trace reveals this immediately while aggregate latency metrics might not.

## Quality Signals

Runtime metrics measure speed and availability. They do not measure whether the retrieval found the right content.

Quality signals for RAG include:

- **Reranker score distribution**: if top-1 reranker scores are consistently low (< 0.3), retrieval quality is poor even when volume is high
- **Context length utilization**: if retrieved chunks are consistently empty or very short, the chunking or index has problems
- **Eval score trend** (from Module 11): the most reliable quality signal
- **Negative feedback rate**: users flagging unhelpful responses often correlates with poor retrieval

## Multi-Tenant Isolation Monitoring

In a multi-tenant RAG system, observability should verify that tenant isolation holds:

- all metrics should carry a `tenant` label
- zero-result queries should be analyzed per tenant to catch configuration drift
- index staleness should be tracked per tenant (not just globally)
- ingestion error rates should be compared across tenants to detect tenant-specific issues

A per-tenant dashboard row is more useful than global aggregates for diagnosing tenant-specific degradation.

## Tracing A RAG Query

A well-traced RAG query produces a span tree like:

```
rag.query (75ms total embedding + retrieval)
├── rag.embed_query (45ms)
├── rag.vector_search (18ms, chunks_returned=10)
└── rag.rerank (12ms, chunks_after=5, top_score=0.82)
```

These spans, when correlated with the parent `llm.generate` span, give the full latency waterfall for the request.

## Staleness Alert Design

Index freshness is a safety property for RAG. Documents that have been updated since the last ingest may contain stale information that the model will present as current.

Alert design:

```yaml
# Prometheus alerting rule
- alert: RAGIndexStale
  expr: (time() - rag_index_last_updated_timestamp) > 86400
  for: 15m
  labels:
    severity: warning
  annotations:
    summary: "RAG index for {{ $labels.tenant }} is stale"
    description: "Index last updated {{ $value | humanizeDuration }} ago"
    runbook: "https://wiki/rag-index-freshness"
```
