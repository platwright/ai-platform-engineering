# Project 01 - Unified Model Client

## Goal

Build one application-facing interface that can call multiple model providers through the same abstraction.

This project is intentionally small, but it represents an important architectural step. Before you build a full AI gateway or platform API, an application team often needs a local, testable, provider-agnostic model client.

## What You Will Build

The project includes:

- a configuration-driven unified model client
- mock providers for local development and failure simulation
- an optional OpenAI-compatible provider path
- a CLI for synchronous chat requests
- a local HTTP API exposing `/api/chat`, `/providers`, and `/healthz`
- JSON run artifacts for response inspection

## Why This Project Matters

Without a stable model access layer, application code often becomes tightly coupled to one provider's transport, auth, and response schema. That makes provider switches, failover, testing, and later platform standardization much harder.

Project 01 solves that problem at the application layer first.

## Project Files

- `app.py`: CLI entry point and local server launcher
- `config/app.example.json`: application and provider configuration
- `prompts/`: prompt artifacts used by the app
- `fixtures/`: mock provider responses
- `unified_model_client/`: provider adapters, config loader, service, and local server code
- `runs/`: generated JSON reports

## Documentation

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Quick Start

List providers:

```bash
python projects/project-01-model-api/app.py list-providers
```

Run a success path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-fast
```

Run a failure path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-rate-limited
```

Serve the local HTTP API:

```bash
python projects/project-01-model-api/app.py serve
```

## Optional Real Provider Path

Set these environment variables if you want to use an OpenAI-compatible endpoint:

- `MODEL_API_URL`
- `MODEL_API_KEY`
- `MODEL_NAME`

Then call:

```bash
python projects/project-01-model-api/app.py chat --provider openai-compatible --message "Explain the role of a prompt layer in an AI application."
```

## Relationship To Module 03

This project is the executable companion to [modules/03-ai-application-architecture/README.md](../../modules/03-ai-application-architecture/README.md). It shows how application APIs, prompt handling, config, and provider abstraction fit together before containerization or Kubernetes enters the picture.