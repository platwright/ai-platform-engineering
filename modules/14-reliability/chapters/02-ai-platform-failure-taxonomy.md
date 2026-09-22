# Chapter 02 - AI Platform Failure Taxonomy

## Why A Taxonomy Matters

A shared taxonomy for AI platform failures does three things: it gives operators a common vocabulary for incident communication, it drives runbook design (each category needs different diagnostic steps), and it enables meaningful failure rate tracking across categories over time.

The six categories below cover the distinct failure types that appear across the platform stack.

## Category 1: Infrastructure Failures

Failures at the compute, memory, container, or network level.

| Failure | Typical Symptom | Key Signal |
|---|---|---|
| GPU out of memory (OOM) | Container restart, CUDA OOM error in logs | `DCGM_FI_DEV_FB_USED` at 100%, container restart counter |
| Container crash | Pod restarting, 5xx responses | `kubectl get pods`, pod restart count |
| Node failure | All pods on node unreachable | Node NotReady status |
| Network partition | Intermittent timeouts between services | Trace spans timing out between specific service pairs |
| Storage failure | Index reads failing, state loss | Disk I/O errors in container logs |

**Recovery pattern**: container restarts are usually automatic. GPU OOM may require reducing batch size or request queue depth. Node failures require pod rescheduling and may temporarily reduce serving capacity.

## Category 2: Provider Failures

Failures in hosted model API services.

| Failure | Typical Symptom | Key Signal |
|---|---|---|
| API timeout | Long-running requests with no response | Gateway timeout counter, provider latency p99 |
| 5xx from provider | Gateway returns error after provider 500 | Provider error rate in gateway logs |
| Rate limit (429) | Requests rejected with 429 status | Rate limit event counter per tenant |
| Provider outage | All requests to provider failing | Provider health check, status page |
| Silent model update | Response behavior changes without API change | Eval score drift, canary prompt similarity drop |

**Recovery pattern**: timeouts and 5xxs are retriable. Rate limits require backoff and quota review. Outages require fallback to another provider or graceful degradation.

## Category 3: Quality Failures

Failures in output quality that do not produce HTTP error codes.

| Failure | Typical Symptom | Key Signal |
|---|---|---|
| Hallucination increase | Users reporting incorrect facts | Eval score drop, negative feedback rate rise |
| Retrieval degradation | RAG responses less relevant | Reranker score distribution shift, eval RAG score drop |
| Format regression | Model stops producing expected JSON structure | Structured output parse error rate |
| Behavioral shift | Model behaves differently than expected | Canary prompt semantic similarity drop |
| Prompt regression | New prompt version produces worse outputs | Eval score comparison to baseline |

**Recovery pattern**: rollback to previous prompt version, revert model version pin, investigate RAG index staleness. Quality failures require investigation, not just restarts.

## Category 4: Configuration Failures

Failures caused by incorrect or misapplied configuration.

| Failure | Typical Symptom | Key Signal |
|---|---|---|
| Wrong model version | Different behavior than expected | Model version in response metadata |
| Generation parameter change | Response length, randomness, or format changed | Parameter logging per request |
| Routing misconfiguration | Traffic going to wrong provider | Route selection logs |
| Missing environment variable | Application startup failure or incorrect behavior | Container startup logs |
| Config drift between environments | Works in staging, fails in production | Config comparison audit |

**Recovery pattern**: identify the config change (git history, deployment log), revert the specific configuration, re-deploy.

## Category 5: Data Failures

Failures caused by data quality or data availability problems.

| Failure | Typical Symptom | Key Signal |
|---|---|---|
| Stale RAG index | Responses reference outdated information | `rag_index_last_updated_timestamp` |
| Missing documents | Zero retrieval results for valid queries | Zero-result query counter |
| Embedding mismatch | Re-indexed documents with different embedding model | Unexpected retrieval quality drop after re-ingest |
| Tenant boundary violation | Documents from wrong tenant returned | Per-tenant retrieval auditing |
| Corrupt index | Retrieval errors or unexpected crash | Vector DB health logs |

**Recovery pattern**: re-ingest the affected tenant, validate the index, fix the ingestion pipeline root cause.

## Category 6: Cascading Failures

Failures that amplify through the system, often triggered by one of the above categories.

| Failure | How It Cascades |
|---|---|
| Retry storm | Provider timeout → all clients retry → provider receives 10× normal load → further timeouts |
| Queue flood | Slow model serving → requests queue → memory fills → container OOM → restart → cold start → more queueing |
| Cache stampede | Cache expiry → all requests miss → load spike on uncached backend → latency spike → timeouts |
| Token budget exhaustion | One tenant's runaway generation → approaches quota → rate limit fires for all requests |

**Prevention**: circuit breakers prevent retry storms. Queue depth limits prevent queue floods. Staggered cache TTLs prevent stampedes. Per-tenant quotas prevent shared exhaustion.

## Failure Classification In Practice

Not every failure fits neatly into one category. A stale RAG index (data failure) caused by an ingestion pipeline crash (infrastructure failure) that was triggered by a disk full event (infrastructure failure) spans multiple categories. What matters is identifying the root cause category for the post-mortem, even if the chain involves multiple layers.

Use the taxonomy as a starting-point lens for triage, not a strict classification system.
