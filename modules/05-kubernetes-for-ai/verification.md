# Module 05 Verification

## Required Checks

Render the manifests:

```bash
kubectl kustomize platform/kubernetes/sample-chat
```

Expected result:

- all resources render successfully
- the stack includes Deployments, Services, a Job, a StatefulSet, an HPA, an Ingress, and configuration resources

Optional cluster deployment:

```bash
kubectl apply -k platform/kubernetes/sample-chat
```

Expected result if using a local cluster:

- Pods start for `sample-chat`, `model-api`, and `qdrant`
- the batch Job completes or runs to completion
- the sample chat API is reachable through port-forward or ingress

## Understanding Check

You should be able to explain:

- why the sample chat app uses a Deployment
- why Qdrant uses a StatefulSet and persistent storage
- why the batch summary path is a Job
- how the ConfigMap and Secret template influence runtime behavior
- why user-facing AI paths need careful readiness and networking design