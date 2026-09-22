# Module 01 Architecture

## Mental Model Diagrams

This module is conceptual, but it still benefits from architecture views. The purpose of these diagrams is to show the control points a platform engineer should care about before specific tools enter the picture.

## AI Domain Relationship

```mermaid
flowchart TD
    AI[Artificial Intelligence]
    ML[Machine Learning]
    DL[Deep Learning]
    GenAI[Generative AI]
    FM[Foundation Models]
    LLM[Large Language Models]

    AI --> ML --> DL --> GenAI --> FM --> LLM
```

## Training And Inference As Different Systems

```mermaid
flowchart LR
    Dataset[Dataset] --> TrainJob[Training Job]
    TrainJob --> GPUCluster[GPU Cluster]
    GPUCluster --> Checkpoint[Checkpoint]
    Checkpoint --> ModelArtifact[Model Artifact]

    Request[User or App Request] --> InferenceAPI[Inference API]
    InferenceAPI --> LoadedModel[Loaded Model]
    LoadedModel --> Tokens[Prediction or Tokens]
```

## Mini Project Flow

```mermaid
flowchart LR
    PromptFile[Prompt File] --> Observer[AI Workload Observer]
    Observer --> Mock[Mock Fixture]
    Observer --> Endpoint[OpenAI-Compatible Endpoint]
    Mock --> Report[Run Report JSON]
    Endpoint --> Report
```

## Lifecycle View

```mermaid
flowchart LR
    Experiment --> Develop --> Evaluate --> Package --> Deploy --> Serve --> Observe --> Improve
```

## What To Notice

- training and inference are adjacent, but not interchangeable workloads
- the inference interface becomes a platform surface as soon as multiple teams or models exist
- observability starts at the first API call, not only after Kubernetes is introduced
- the lifecycle is a control loop, not a one-way pipeline