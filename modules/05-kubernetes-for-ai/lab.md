# Module 05 Lab

## Goal

Render, inspect, and optionally deploy the sample chat Kubernetes stack.

## Outcome

By the end of this lab, you should have:

- rendered the full manifest set locally
- understood how the stack maps onto Kubernetes objects
- optionally loaded the images into a local cluster and deployed the stack

## Step 1 - Review The Manifest Set

Start with:

- [platform/kubernetes/sample-chat/README.md](../../platform/kubernetes/sample-chat/README.md)
- [applications/sample-chat/README.md](../../applications/sample-chat/README.md)

## Step 2 - Render The Stack

```bash
kubectl kustomize platform/kubernetes/sample-chat
```

This should render a namespace, Deployments, Services, an HPA, a Job, a StatefulSet, and an Ingress.

## Step 3 - Optional Local Cluster Path

If you have `kind` available:

```bash
kind create cluster --name aipe
docker build -t aipe/project-01-model-api:local projects/project-01-model-api
docker build -t aipe/sample-chat:local applications/sample-chat
kind load docker-image aipe/project-01-model-api:local --name aipe
kind load docker-image aipe/sample-chat:local --name aipe
kubectl apply -k platform/kubernetes/sample-chat
```

## Step 4 - Inspect Rollout

```bash
kubectl get pods -n aipe-sample-chat
kubectl get svc -n aipe-sample-chat
kubectl get job -n aipe-sample-chat
kubectl get statefulset -n aipe-sample-chat
```

## Step 5 - Access The App

If you are not using an Ingress controller locally, port-forward the service:

```bash
kubectl port-forward -n aipe-sample-chat svc/sample-chat 8080:8080
```

Then send a request:

```bash
curl -X POST http://127.0.0.1:8080/api/chat -H "Content-Type: application/json" -d "{\"message\":\"Explain why Jobs and Deployments are different in Kubernetes.\"}"
```

## Step 6 - Inspect The Batch Job

Review the batch summary job logs and compare its behavior to the user-facing service pods.

## Step 7 - Reflect

Write down:

- which parts of the stack are stateless
- which parts are stateful
- which parts would change once GPU-backed serving arrives later in the course