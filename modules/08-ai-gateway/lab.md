# Module 08 Lab

## Goal

Run the local AI gateway, route requests through it, and observe caching, fallback, and usage metrics.

## Step 1 - Review The Assets

- [platform/docker/ai-gateway-service/app.py](../../platform/docker/ai-gateway-service/app.py)
- [platform/docker/ai-gateway-stack.compose.yml](../../platform/docker/ai-gateway-stack.compose.yml)
- [platform/kubernetes/ai-gateway/README.md](../../platform/kubernetes/ai-gateway/README.md)

## Step 2 - Inspect Routing Decisions

```bash
python platform/docker/ai-gateway-service/app.py route --message "Explain AI gateway routing."
python platform/docker/ai-gateway-service/app.py route --message "Explain how to handle private confidential data."
```

## Step 3 - Run The Gateway Stack

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml up --build
```

## Step 4 - Send Requests Through The Unified Endpoint

```bash
curl -X POST http://127.0.0.1:8090/api/chat -H "Content-Type: application/json" -d "{\"application_id\":\"sample-chat\",\"message\":\"Explain model routing in an AI gateway.\"}"
```

## Step 5 - Observe Cache Or Metrics

Repeat the same request and then inspect:

```bash
curl http://127.0.0.1:8090/metrics
```

Look for request totals, provider usage, cache hits, and fallback counts.

## Step 6 - Render The Kubernetes Stack

```bash
kubectl kustomize platform/kubernetes/ai-gateway
```

## Step 7 - Reflection

Write down:

- which requests should route cheaply versus conservatively
- when fallback should happen automatically
- what additional metrics or controls you would add before production