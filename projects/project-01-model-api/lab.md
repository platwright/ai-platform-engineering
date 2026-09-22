# Project 01 Lab

## Goal

Run the unified model client through the same application-facing interface against multiple provider aliases.

## Step 1 - List Providers

```bash
python projects/project-01-model-api/app.py list-providers
```

## Step 2 - Run The Default Success Path

```bash
python projects/project-01-model-api/app.py chat --provider acme-fast
```

## Step 3 - Compare Another Successful Provider

```bash
python projects/project-01-model-api/app.py chat --provider acme-reliable --message "Explain why configuration is part of runtime behavior in AI applications."
```

## Step 4 - Exercise The Failure Path

```bash
python projects/project-01-model-api/app.py chat --provider acme-rate-limited
```

## Step 5 - Optional HTTP API

Start the local server:

```bash
python projects/project-01-model-api/app.py serve
```

Then send a request:

```bash
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"provider\":\"acme-fast\",\"message\":\"Explain the anatomy of an AI application.\"}"
```

## Reflection

Write down:

- what changed when you switched providers
- what stayed stable in the interface
- which fields would become logs, metrics, and traces later