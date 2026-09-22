# Module 05 Architecture

## Sample Chat Stack On Kubernetes

```mermaid
flowchart LR
    User[User or curl] --> Ingress[Ingress]
    Ingress --> ChatSvc[Sample Chat Service]
    ChatSvc --> ChatPods[Sample Chat Deployment]
    ChatPods --> ModelSvc[Model API Service]
    ModelSvc --> ModelPods[Model API Deployment]
    ChatPods --> QdrantSvc[Qdrant Service]
    QdrantSvc --> QdrantSet[Qdrant StatefulSet]
```

## Mixed Workload Types

```mermaid
flowchart TB
    Deploy[Deployments<br/>sample-chat, model-api]
    Job[Job<br/>batch-summary]
    Stateful[StatefulSet<br/>qdrant]

    Deploy --> Service[Services]
    Job --> Service
    Stateful --> PVC[Persistent Storage]
```

## Control And Config Objects

```mermaid
flowchart LR
    ConfigMap[ConfigMap] --> Chat[Sample Chat Deployment]
    Secret[Secret Template] --> Model[Model API Deployment]
    HPA[HPA] --> Chat
```

## What To Notice

- the application path is still recognizably the same as in Module 04
- Kubernetes adds control over rollout, scaling, and service discovery
- stateful infrastructure is modeled explicitly rather than hidden inside app pods