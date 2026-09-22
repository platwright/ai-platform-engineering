# Sample Agent Application

## Goal

Provide a small application-facing wrapper around Project 04 so learners can interact with the agent platform through a simpler surface.

## What It Does

- accepts an agent objective from a CLI or HTTP API
- forwards that objective to Project 04
- returns the final response and execution summary
- stores local run artifacts for inspection

## Files

- `app.py`: CLI entry point and local server launcher
- `config/app.example.json`: application configuration
- `runs/`: generated request artifacts

## Quick Start

Start the agent platform service first, then run:

```bash
python applications/sample-agent/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

## Why It Matters

This application lets later modules discuss agent product flows separately from the shared platform service that actually owns tool policy and approval.