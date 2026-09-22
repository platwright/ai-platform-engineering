# Chapter 05 - Streaming

## What Streaming Is

By default, a model completes the entire response before sending it. The client waits until generation finishes before seeing any output.

Streaming changes this: the model sends each token as it is generated using server-sent events (SSE) or a similar chunked transfer mechanism.

```
Without streaming:
Client waits 3 seconds → entire response arrives at once

With streaming:
Client sees first token in 400ms → tokens arrive continuously until generation completes
```

## Why Streaming Matters

For interactive applications, streaming dramatically improves perceived responsiveness. Users can start reading before generation ends.

For platform engineers, streaming changes several concerns:

- load balancers and proxies must support long-lived connections
- AI gateways must pass through chunked responses without buffering
- latency metrics split into TTFT and total generation time
- token-level usage accounting must aggregate across the stream
- logging and cost attribution need complete buffering on the platform side

## How SSE Works For LLMs

Streaming uses the HTTP server-sent events format:

```
HTTP/1.1 200 OK
Content-Type: text/event-stream
Transfer-Encoding: chunked

data: {"id":"...","choices":[{"delta":{"role":"assistant","content":"The"},...}]}

data: {"id":"...","choices":[{"delta":{"content":" inference"},...}]}

data: {"id":"...","choices":[{"delta":{"content":" gateway"},...}]}

data: [DONE]
```

Each `data:` line contains a partial completion chunk. The `[DONE]` sentinel marks the end of the stream.

Clients accumulate these chunks into the final response text.

## TTFT vs End-to-End Latency

Time to first token (TTFT) is the elapsed time from when the request is sent until the first generated token arrives. It measures:

- request transmission time
- model preprocessing and prompt encoding time
- time to start generating

End-to-end latency is the total time until the last token arrives. It adds:

- generation time for all output tokens
- network transmission for all chunks

For a typical interactive application:

```
TTFT:              300–800ms   ← user perceives this as responsiveness
Token rate:        40–80 tok/s ← determines reading pace and total wait
End-to-end:        TTFT + (output_tokens / token_rate)
```

A model with a slow TTFT but fast token rate can still feel sluggish. A model with fast TTFT but slow token generation feels different: the response starts appearing quickly but then takes a while to finish.

## Platform Concerns With Streaming

### Load Balancer and Proxy Compatibility

HTTP proxies and load balancers often buffer responses before forwarding them. This defeats streaming entirely.

Platform configurations must ensure:

- no response buffering on the proxy layer
- connection timeout is long enough for the full generation
- WebSocket or HTTP/2 support if used for long-running streams

### AI Gateway Pass-Through

AI gateways that buffer requests before forwarding break the streaming experience. Production gateways should use pass-through streaming, relaying chunks from the upstream model server immediately.

Rate limiting and usage accounting must still work even when the gateway does not buffer. This is typically done by:

- counting tokens on the streaming path using the usage field in the final chunk
- or using an async counting mechanism that does not block the stream

### Logging and Observability

Platforms typically want to log complete request/response pairs. In streaming mode, the complete response is only known at the end of the stream.

Platform-level logging must:

- buffer the stream internally to assemble the complete response
- not block the pass-through to the client while doing so
- capture the final usage fields from the stream's last chunk

A typical pattern uses a tee-style reader that copies stream chunks to the client and to an internal buffer simultaneously.

### Error Handling Mid-Stream

Errors can occur after streaming has started, meaning the client has already received partial output. This is an awkward failure mode.

Best practices:

- send errors in a structured final chunk if the protocol supports it
- monitor for incomplete stream patterns on the platform side
- surface mid-stream failure events in observability dashboards separately from request-level errors

## When Not To Use Streaming

Streaming is not always the right choice:

| Scenario | Recommendation |
|---|---|
| Batch processing jobs | Buffered: simpler to handle at volume |
| Evaluation pipelines | Buffered: completions need to be fully assembled for scoring |
| Short factual lookups | Optional: TTFT gain is small when total generation is brief |
| Rate-limited budget accounting | Requires buffered completion counts |
| Downstream JSON parsing | Buffer the full response before parsing |

## Token Rate as a Serving Metric

Token generation speed is a key inference performance metric:

- **Tokens per second (tok/s)**: how fast the model generates output tokens
- Affected by model size, quantization, hardware, batch size, and KV cache state
- Directly determines perceived streaming speed for users

A model serving at 20 tok/s produces about one word every 150ms — slow enough to feel like watching someone type character by character. A model at 80 tok/s fills a screen paragraph in about 3 seconds — comfortable for interactive use.

This is why model serving decisions affect product experience, not just infrastructure cost.

## Summary

| Concern | Streaming Impact |
|---|---|
| User experience | Major: TTFT drives perceived responsiveness |
| Infrastructure | Proxies, gateways, and LBs must support long-lived connections |
| Observability | Latency splits into TTFT and generation rate |
| Logging | Platform must buffer independently of client pass-through |
| Cost accounting | Usage data arrives at end of stream, must be captured |
| Error handling | Mid-stream failures are harder to recover from gracefully |
