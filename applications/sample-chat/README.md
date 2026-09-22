# Sample Chat Application

## Goal

Provide a small application-layer HTTP service that wraps Project 01 and exposes a chat-oriented API surface.

This application is intentionally simple. It exists so later modules can package, containerize, compose, and deploy a real application instead of only talking about abstract architecture.

## What It Does

- exposes a local HTTP API for chat requests
- loads an application prompt template from files
- calls Project 01 over HTTP as its model access layer
- produces JSON run artifacts for local inspection
- separates application behavior from provider-specific model integration

## Files

- `app.py`: CLI entry point and local server launcher
- `config/app.example.json`: application configuration
- `prompts/`: prompt assets for the application layer
- `runs/`: generated request artifacts

## Runtime Assets

- [platform/docker/sample-chat-stack.compose.yml](../../platform/docker/sample-chat-stack.compose.yml): local Compose stack for Module 04
- [platform/kubernetes/sample-chat/README.md](../../platform/kubernetes/sample-chat/README.md): Kubernetes manifest set for Module 05

## Quick Start

The sample chat application depends on Project 01 running as its backend model API.

Start Project 01:

```bash
python projects/project-01-model-api/app.py serve
```

In another terminal, start the sample chat app:

```bash
python applications/sample-chat/app.py serve
```

Then send a request:

```bash
curl -X POST http://127.0.0.1:8080/api/chat -H "Content-Type: application/json" -d "{\"message\":\"Explain why stateless processes are useful in AI applications.\"}"
```

## Why It Matters

This application is the bridge between Module 03 and the runtime-focused modules.

- Module 03 uses it to make application architecture concrete.
- Module 04 uses it as the first application to containerize and compose.
- Module 05 uses it as the first application stack to move to Kubernetes.

## Notes

- Run artifacts under `runs/` are ignored by Git.
- The sample app uses only the Python standard library.
- The backend model access layer stays in Project 01 so the separation of concerns remains visible.