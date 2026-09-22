# Project 04 - Agent Platform

## Goal

Build a safer agent-oriented platform path that can query platform services through a discoverable tool catalog, apply policy, and require approval for destructive operations.

The project uses Project 03 and the AI gateway as platform services the agent can safely query.

## What You Will Build

- a local agent platform service with a tool registry
- safe tool execution against Project 03 and the AI gateway
- approval gates for destructive actions
- run artifacts that capture decisions, tool calls, and results

## Why This Project Matters

Agent infrastructure is not only about model calls. It is about tool discovery, authorization, policy, state, auditability, and operational controls. This project makes those concerns visible early.

## Project Files

- `app.py`: CLI entry point and HTTP API
- `config/app.example.json`: platform configuration
- `runs/`: generated agent run artifacts

## Documentation

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Quick Start

List the available tools:

```bash
python projects/project-04-agent-platform/app.py list-tools
```

Run a safe query objective:

```bash
python projects/project-04-agent-platform/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

Attempt a destructive objective without approval:

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb
```

## Relationship To Module 10

This project is the executable companion to [modules/10-agent-platform/README.md](../../modules/10-agent-platform/README.md). It focuses on safe tool use, policy, approval, and platform querying rather than on agent hype.