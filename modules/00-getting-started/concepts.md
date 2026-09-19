# Module 00 Concepts

## The Core Job

AI platform engineering is the discipline of making AI capabilities usable, reliable, secure, and scalable for application teams.

That means the platform engineer usually cares less about inventing a new model and more about:

- where models run
- how requests reach them
- how teams authenticate and authorize access
- how prompts, tools, and retrieval layers are versioned
- how usage, latency, failures, and costs are observed
- how the overall platform is delivered safely and repeatedly

## The Three Layers

This course uses a simple three-layer model.

### 1. AI Application Layer

This is where product-facing experiences live:

- chat interfaces
- copilots
- document assistants
- internal knowledge tools
- agent-style workflows

### 2. AI Platform Layer

This is the main focus of the course:

- model gateways
- RAG services
- agent runtime controls
- prompt and evaluation workflows
- observability, policy, and cost controls
- developer self-service abstractions

### 3. Infrastructure Layer

This is the execution substrate:

- compute
- Kubernetes
- GPUs
- storage
- networking
- secrets and identity foundations

## Why Platform Engineers Need AI Fundamentals

If you do not understand tokens, context windows, embeddings, streaming, model latency, and GPU constraints, it becomes difficult to design sane infrastructure or troubleshoot production failures.

The course therefore teaches enough AI to make platform decisions defensible.

## Why The Course Is Local First

Starting with local tooling keeps the first iterations fast and low cost. Learners can focus on system behavior before adding cloud complexity.

Later modules will add:

- Kubernetes
- GPUs
- gateway policy
- RAG operations
- agent safety
- observability and SLOs

## The Acme AI Narrative

Instead of many disconnected demos, the course follows Acme AI, a fictional organization that needs a reusable internal AI platform. Each module adds one capability to the same platform story.