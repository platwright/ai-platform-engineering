# Chapter 08 - Inference Scheduling and Batching

## Why Batching Matters For Inference

GPUs are highly parallel processors. A single matrix multiplication on a GPU takes nearly the same time whether it processes 1 row or 32 rows. This means serving 32 tokens from 32 different requests simultaneously is nearly as fast as serving 1 token from 1 request.

Batching exploits this parallelism to improve throughput. The challenge is doing it without unacceptably increasing latency for individual requests.

## Static Batching (Naive)

Static batching groups requests together and processes them as a unit:

```
Time 0:  Receive requests A, B, C, D
Time 0:  Batch [A, B, C, D] → start processing
Time 5s: Requests A, B complete (short)
         C, D still running (longer)
         A, B wait for C, D to finish before being returned
Time 10s: C, D complete → return all four
```

Problems:
- Short requests wait for long requests (TTFT increases for short requests)
- Batch efficiency drops when requests have very different lengths
- New requests arriving during batch processing must wait for the entire batch to complete

## Dynamic Batching

Dynamic batching assembles batches from the request queue based on size and timing constraints:

```
Batch window: 20ms
Max batch size: 8

At t=0ms:  3 requests arrive
At t=10ms: 2 more arrive → batch of 5 sent at t=20ms
At t=22ms: 4 more arrive → batch of 4 sent at t=40ms
```

Dynamic batching reduces TTFT compared to static batching but still has the padding problem: shorter sequences must be padded to the length of the longest sequence in the batch.

## Continuous Batching (Iteration-Level Batching)

Continuous batching is the key innovation in modern LLM serving. It schedules at the token generation iteration level rather than at the request level:

```
Iteration 1: Generate token N for requests A, B, C, D, E
Iteration 2: A completes → slot freed → request F enters
             Generate token N+1 for B, C, D, E, F
Iteration 3: Generate token N+2 for B, C, D, E, F...
```

Benefits:
- GPU never sits idle waiting for a full batch to complete
- Short requests finish early and free slots immediately
- TTFT is dramatically lower than static batching
- Throughput is significantly higher than dynamic batching

vLLM implements continuous batching and it is the reason for its significant performance advantages over earlier serving approaches.

## Chunked Prefill

Standard prefill processes all input tokens for a request before generating any output tokens. For long prompts, this delays TTFT for other requests in the batch.

Chunked prefill splits the prefill phase into smaller chunks:

```
Without chunked prefill:
  Prefill 4096 tokens (1200ms) → then generate → other requests wait 1200ms

With chunked prefill:
  Prefill first 512 tokens (150ms)
  Interleave: generate some tokens for other requests
  Prefill next 512 tokens
  Continue interleaving...
```

This reduces TTFT for low-latency requests even when long-context requests are being processed concurrently. Enable in vLLM with `--enable-chunked-prefill`.

## Speculative Decoding

Speculative decoding uses a small "draft" model to generate multiple token candidates, which a larger "verifier" model accepts or rejects in parallel:

```
Draft model: generates candidates [tok1, tok2, tok3, tok4, tok5]
Verifier:    checks all 5 in one forward pass
             → accepts [tok1, tok2, tok3], rejects [tok4, tok5]
             → generate next draft from tok3
```

When draft tokens are frequently accepted (high acceptance rate), 2–4× throughput improvement is achievable. Acceptance rate depends on how similar the draft model's distribution is to the verifier's.

Use speculative decoding when:
- output is predictable or formulaic (code, structured data)
- you have a small draft model (same family, 1/4–1/10 the size) available
- throughput is the primary concern over TTFT

## Scheduling Summary

| Strategy | TTFT | Throughput | Complexity |
|---|---|---|---|
| Static batching | High | Medium | Low |
| Dynamic batching | Medium | High | Medium |
| Continuous batching | Low | High | Low (built into vLLM) |
| Chunked prefill | Very low for co-located short requests | High | Low (flag in vLLM) |
| Speculative decoding | Lower | Much higher | High (needs draft model) |

For most deployments: use continuous batching (vLLM default) with chunked prefill enabled. Evaluate speculative decoding only when throughput is critical and a suitable draft model is available.
