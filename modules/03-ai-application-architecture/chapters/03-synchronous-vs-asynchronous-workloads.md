# Chapter 3.3 - Synchronous vs Asynchronous Workloads

## The Core Decision

The main question is simple: does the caller wait for the result right now?

If yes, the workload is synchronous. If not, it is asynchronous.

## Synchronous AI Workloads

Examples:

- chat interactions
- real-time extraction during a user workflow
- live moderation checks

Characteristics:

- user experience tied directly to latency
- timeouts matter immediately
- retries can increase user-visible delays and cost
- observability must support request-level diagnosis

## Asynchronous AI Workloads

Examples:

- document indexing
- batch embeddings
- offline summarization
- periodic evaluation runs

Characteristics:

- queue or job friendly
- throughput often matters more than single-request latency
- retries and backoff policies differ from user-facing flows
- progress tracking and idempotency matter more

## Mixed Systems

Many AI applications need both modes.

Example:

- synchronous chat query path
- asynchronous document ingestion and indexing path

Putting both through one web request path usually leads to poor design.

## Operational Implications

Synchronous paths care most about:

- latency
- concurrency
- request timeouts
- graceful degradation

Asynchronous paths care most about:

- queue depth
- worker throughput
- retry policy
- completion tracking

## Platform Takeaway

Choosing sync versus async is not only an implementation detail. It shapes API design, scaling strategy, storage usage, user expectations, and incident response.