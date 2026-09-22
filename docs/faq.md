# FAQ

## Course Content

### Do I Need To Be A Data Scientist?

No. This course is for engineers who need to build and operate the platform around AI workloads. Data science and model training are explicitly outside scope. You need to understand AI workload behavior well enough to make platform decisions, not well enough to design model architectures.

### Is This Only About LLM APIs?

No. The course covers model serving infrastructure, GPU and accelerator management, RAG platforms, agent systems, observability, security, reliability, FinOps, and developer platform design. LLM API usage is the starting point, not the destination.

### Why Does Module 03 Come After Module 01 With Module 02 In Between?

Module 01 establishes the AI workload mental model. Module 02 covers LLM-specific runtime behavior (tokenization, generation parameters, tool calling, streaming). Module 03 then builds the application architecture on top of that foundation. They build on each other in sequence.

### Can I Skip To Kubernetes Or GPUs?

You can, but the modules from 00 through 03 exist to build the workload mental model that makes later infrastructure decisions sensible rather than mechanical. Learners who skip them often find themselves applying generic DevOps thinking to AI-specific problems and getting confused by the differences.

### Do I Need To Complete Every Module In Order?

The order is intentional, but learners with existing expertise in particular areas can skip or skim earlier modules. The [learning paths](learning-paths.md) document provides role-specific sequences for common starting points.

### How Long Does The Full Course Take?

Each module estimates 4 to 8 hours. The full course across 18 modules is roughly 100 to 130 hours of active work. Most learners spread this over several months alongside their regular work.

### Is There A Certificate Or Credential?

Not currently. The course is designed to produce portfolio artifacts and a platform narrative you can discuss in interviews. The capstone module (Module 18) guides you through assembling that artifact.

---

## Infrastructure and Setup

### Do I Need A GPU?

Not for the early modules. The course is local-first and uses CPU-friendly or hosted provider paths where possible. Module 06 (GPU and Accelerators) and Module 07 (Model Serving) introduce GPU concepts, but the core labs can be done without dedicated GPU hardware using Ollama or mock serving paths.

### Can I Use A Cloud Provider Instead Of Local Docker?

Yes. The course starts local-first to reduce cost and dependency on external accounts, but every concept applies equally to cloud-hosted Kubernetes, managed vector databases, and hosted model serving. The local implementation is a teaching simplification.

### Do I Need Ollama?

Ollama is recommended but not required for the early modules. It provides a local model endpoint that is useful for experimenting with real inference behavior, but mock providers in Project 01 cover most of the same learning surface without requiring a downloaded model.

### My Docker Compose Stack Won't Start

Start with these checks:

1. Is Docker running? (`docker info` should succeed)
2. Do the required ports conflict with existing services? Check `docker compose -f <file> config` to see which ports are used.
3. Did the build fail? Check `docker compose logs` for build errors.
4. Do you have enough disk space? Model weights and container layers are large.

See [docs/troubleshooting.md](troubleshooting.md) for more detailed diagnostics.

### I Don't Have Enough RAM For The Labs

The early modules run on 8 GB RAM. Most module labs with multiple containers need 12–16 GB. If you are resource-constrained, run services one at a time rather than as a full stack.

---

## Projects and Code

### What Is The Difference Between A Module And A Project?

Modules teach concepts through chapters, labs, and challenges. Projects are larger deliverables that build interview-ready platform artifacts. Each project is the executable companion to a set of modules. The full sequence is: learn concepts in modules → build the project → the project becomes portfolio work.

### Can I Use The Projects At Work?

The project code is MIT-licensed. You can adapt it for work purposes. Note that the projects are intentionally simplified for learning. They use mock providers, lightweight local embeddings, and simple state management. Production use would require replacing those components.

### Project 01 Returns An Error About A Missing Config

Copy the example config before running:

```bash
cp projects/project-01-model-api/config/app.example.json projects/project-01-model-api/config/app.json
```

The application reads from `app.json`, which is gitignored so you can customize it without polluting upstream.

### How Do I Reset A Project To Its Starting State?

Delete the generated artifacts in the `runs/` and `state/` directories and recreate the config from the example:

```bash
rm -rf projects/project-XX-*/runs/*
rm -rf projects/project-XX-*/state/*
```

---

## Learning and Content

### Why Does The Course Use A Fictional Company?

The Acme AI narrative keeps the modules connected. Instead of 18 disconnected tutorials, the platform grows continuously. This makes it possible to reason about interfaces between platform capabilities, ownership of shared services, and production tradeoffs between different design choices.

### Some Module Chapters Are Long. Do I Need To Read Everything?

The chapters are written to be read in order and build on each other. For modules where you already have background, reading the `concepts.md` file and doing the lab may be sufficient. The chapters provide the depth you need to answer the knowledge check questions at the end of each README.

### Why Are The Labs Local-First Instead Of Using Real Cloud Services?

Three reasons: cost, reproducibility, and accessibility. A local-first path means learners anywhere in the world can follow the course without a credit card or cloud account. Real cloud services are introduced as optional extensions in later modules.

### What Is The Workbook For?

Your fork or local clone of the repository is your working notebook. The setup scripts create `progress/`, `my-notes/`, and `my-solutions/` directories. Use them to track where you are, capture decisions and reflections, and store your challenge answers. These directories are gitignored in the upstream repository.

### Why Are Modules 02 and 11-18 Not Yet Complete?

The repository is built progressively following the phases in [ROADMAP.md](../ROADMAP.md). Modules 00 through 10 are complete. Modules 11 through 18 are planned with full structural descriptions. The remaining content will be authored in phases 5 and 6.

### How Can I Contribute?

Read [CONTRIBUTING.md](../CONTRIBUTING.md). Good contributions include fixing broken lab steps, improving explanations, adding missing verification steps, and adding references. The most valuable contributions keep the local-first learning path intact and align with the Acme AI narrative.
