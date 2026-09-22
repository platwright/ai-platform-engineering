# kubectl For AI Platform Operations Cheatsheet

## Pod Diagnostics

```bash
# Get pods in a namespace
kubectl get pods -n <namespace>

# Describe a pod (scheduling, events, resource requests)
kubectl describe pod <pod-name> -n <namespace>

# Get logs from a running pod
kubectl logs <pod-name> -n <namespace>

# Follow logs
kubectl logs -f <pod-name> -n <namespace>

# Get logs from a specific container in a pod
kubectl logs <pod-name> -c <container-name> -n <namespace>

# Get previous container logs (after crash)
kubectl logs <pod-name> --previous -n <namespace>
```

## GPU Resource Inspection

```bash
# Check GPU resource availability on nodes
kubectl describe nodes | grep -A5 "Allocatable"

# Check GPU requests and limits on pods
kubectl get pods -n <namespace> -o json | jq '.items[].spec.containers[].resources'

# Check GPU node labels
kubectl get nodes --show-labels | grep nvidia

# Check node GPU capacity
kubectl get nodes -o custom-columns=NAME:.metadata.name,GPU:.status.capacity."nvidia\.com/gpu"
```

## Checking Pending Pods

```bash
# Get all non-running pods
kubectl get pods --all-namespaces --field-selector=status.phase!=Running

# Describe a pending pod to see why it is not scheduling
kubectl describe pod <pod-name> -n <namespace> | grep -A10 Events
```

## Common Pending Reasons

| Message | Cause | Fix |
|---|---|---|
| `Insufficient nvidia.com/gpu` | No GPU nodes available | Add GPU node or reduce request |
| `node(s) had taint` | Node has untolerated taint | Add toleration to pod spec |
| `Insufficient memory` | Not enough RAM on any node | Reduce memory request or add node |
| `0/1 nodes are available` | No nodes match required selectors | Check nodeSelector and labels |

## Port Forwarding For Local Testing

```bash
# Forward model serving port
kubectl port-forward svc/vllm-service 8001:8001 -n model-serving

# Forward AI gateway port
kubectl port-forward svc/ai-gateway 8080:8080 -n gateway

# Forward Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n observability
```

## Kustomize Operations

```bash
# Render manifests without applying
kubectl kustomize platform/kubernetes/<directory>

# Apply with kustomize
kubectl apply -k platform/kubernetes/<directory>

# Dry run apply
kubectl apply -k platform/kubernetes/<directory> --dry-run=client
```

## Useful Resource Summaries

```bash
# Top nodes (CPU/memory)
kubectl top nodes

# Top pods in a namespace
kubectl top pods -n <namespace>

# Get events sorted by time
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Get all resources in a namespace
kubectl get all -n <namespace>
```

## Deployment Operations

```bash
# Check rollout status
kubectl rollout status deployment/<deployment-name> -n <namespace>

# Roll back a deployment
kubectl rollout undo deployment/<deployment-name> -n <namespace>

# View rollout history
kubectl rollout history deployment/<deployment-name> -n <namespace>

# Scale a deployment
kubectl scale deployment/<deployment-name> --replicas=3 -n <namespace>
```

## Exec Into A Running Container

```bash
# Open a shell in a running pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash

# Run a single command
kubectl exec <pod-name> -n <namespace> -- env | grep MODEL
```

## Checking NVIDIA Device Plugin

```bash
# Verify the device plugin is running
kubectl get pods -n kube-system | grep nvidia

# Check device plugin logs
kubectl logs -n kube-system -l name=nvidia-device-plugin-ds
```
