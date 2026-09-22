# Chapter 06 - Autoscaling with Inference-Specific Metrics

## Why CPU-Based Autoscaling Fails for Model Serving

Kubernetes Horizontal Pod Autoscaler (HPA) defaults to CPU utilization. Model serving pods are not CPU-bound:

- GPU compute does the actual work
- CPU utilization on a model serving pod may be 10–30% even when the GPU is 95% utilized and the queue is full
- CPU spikes briefly during request deserialization and response serialization, then drops
- Scaling decisions based on CPU produce no scaling when needed and unnecessary scaling when not

The correct signal for model serving autoscaling is **queue depth**: `vllm_num_requests_waiting`.

## KEDA for Custom Metric Autoscaling

KEDA (Kubernetes Event-Driven Autoscaling) extends Kubernetes to scale on arbitrary metrics from external sources including Prometheus:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: vllm-serving-scaler
  namespace: model-serving
spec:
  scaleTargetRef:
    name: vllm-serving
  pollingInterval: 15          # check metrics every 15 seconds
  cooldownPeriod: 120          # wait 2 minutes before scaling down
  minReplicaCount: 1
  maxReplicaCount: 5
  triggers:
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.observability:9090
        metricName: vllm_num_requests_waiting
        query: sum(vllm_num_requests_waiting{namespace="model-serving"})
        threshold: "10"        # scale up when queue > 10 requests
```

With this configuration:
- 1 replica when queue depth < 10
- Scales to 2 when queue > 10, to 3 when > 20, etc.
- Scales down after 2 minutes of low queue depth (cooldown prevents thrashing)

## Scale-Up Lag

Adding a GPU replica is not instantaneous:
- pod scheduling: 10–30 seconds
- image pull (if not cached): 1–5 minutes
- model weight loading: 2–15 minutes depending on model size

Total cold-start time: **2–20 minutes** before the new replica is serving.

This means autoscaling cannot respond to sudden bursts. Strategies for handling burst:
- **Warm replicas**: maintain standby replicas that have already loaded the model
- **Minimum replicas**: never scale to zero (keeps at least one warm replica always ready)
- **Predictive scaling**: scale based on historical traffic patterns before load arrives

## Scaling the RAG Embedding Service

If embedding generation is a separate service, it needs independent autoscaling. The embedding service is typically CPU or GPU bound:

- CPU-based embedding (sentence-transformers on CPU): scale on CPU utilization
- GPU-based embedding: scale on GPU utilization or queue depth
- Hosted embedding API: no scaling needed (provider manages capacity)

The embedding service often becomes a bottleneck under high RAG query load because it is called once per query (for query embedding) plus once per chunk during ingestion.

## Autoscaling the Gateway

Gateway autoscaling can use CPU or request rate. Request rate is a more reliable signal:

```yaml
# HPA based on custom requests-per-second metric
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  metrics:
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 500m   # 500 requests per second per pod
```

## Scale-Down Safety

Scaling down removes a GPU replica that may be serving active long-running requests. Configure preStop hooks to drain in-flight requests before pod termination:

```yaml
spec:
  containers:
    - name: vllm
      lifecycle:
        preStop:
          exec:
            command: ["/bin/sh", "-c", "sleep 30"]  # wait for in-flight to complete
  terminationGracePeriodSeconds: 60
```

The termination grace period must be longer than the maximum expected request duration to avoid abrupt termination of in-progress generation.
