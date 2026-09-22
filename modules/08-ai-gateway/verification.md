# Module 08 Verification

## Required Checks

Inspect routing:

```bash
python platform/docker/ai-gateway-service/app.py route --message "Explain AI gateway routing."
```

Render the Compose stack:

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml config
```

Render the Kubernetes manifests:

```bash
kubectl kustomize platform/kubernetes/ai-gateway
```

## Expected Result

- routing decisions print successfully
- Compose renders successfully
- Kubernetes manifests render successfully
- a request sent through the gateway can reach Project 01 and return a normalized response

## Understanding Check

You should be able to explain:

- why the gateway exists
- what determines route selection
- when fallback helps and when it can hide failures
- why rate limits and quotas need explicit scoping
- how caching affects both latency and correctness