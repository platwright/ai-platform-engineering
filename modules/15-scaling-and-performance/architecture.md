# Module 15 Architecture

## End-to-End Latency Waterfall

```
Total latency = 
  [1] network: client → gateway              ~5-20ms
  [2] gateway: auth, routing, request prep   ~5-15ms
  [3] network: gateway → model server        ~1-5ms
  [4] model queue wait                        0ms to ∞ (under load)
  [5] prefill (processing input tokens)       50-500ms (scales with prompt length)
  [6] time to first token (TTFT)              ↑ above + scheduling overhead
  [7] generation (output tokens / tok/s)      100ms to 10s (scales with output length)
  [8] network: model server → gateway        ~1-5ms
  [9] gateway: response assembly             ~1-5ms
  [10] network: gateway → client             ~5-20ms
```

## Scaling Topology

```mermaid
flowchart TB
    LB[Load Balancer] --> App1[App Replica 1]
    LB --> App2[App Replica 2]
    LB --> AppN[App Replica N]

    App1 --> GWPool[AI Gateway Pool]
    App2 --> GWPool
    AppN --> GWPool

    GWPool --> Serve1[Model Server GPU 1]
    GWPool --> Serve2[Model Server GPU 2]
    GWPool --> ServeN[Model Server GPU N]

    Serve1 --> GPU1[(GPU VRAM)]
    Serve2 --> GPU2[(GPU VRAM)]
    ServeN --> GPUN[(GPU VRAM)]
```

## KV Cache Memory Pressure Under Concurrency

```mermaid
xychart-beta
    title "TTFT vs Concurrent Requests"
    x-axis [1, 5, 10, 20, 30, 40, 50]
    y-axis "TTFT (ms)" 0 --> 5000
    line [200, 220, 280, 450, 900, 2100, 4800]
```

TTFT is stable at low concurrency. Once KV cache pressure builds (typically at 70-80% memory), queuing begins and TTFT degrades non-linearly.

## Autoscaling Architecture (KEDA)

```mermaid
flowchart LR
    Metrics[Prometheus Metrics\nvllm_num_requests_waiting] --> KEDA[KEDA ScaledObject]
    KEDA --> HPA[Kubernetes HPA]
    HPA --> Serving[Model Serving Deployment]
    Serving --> GPU1[GPU Pod 1]
    Serving --> GPU2[GPU Pod 2]
    Serving --> GPU3[GPU Pod 3 (new)]
```
