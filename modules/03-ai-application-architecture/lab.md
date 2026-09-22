# Module 03 Lab

## Goal

Use Project 01 to see how an AI application can separate its application-facing interface from provider-specific model integrations.

## Outcome

By the end of this lab, you should have:

- listed the available provider aliases
- run a successful chat request through the unified client
- run a failure path through the same interface
- optionally served the same client behind a local HTTP API
- written down where state and config live in the project architecture

## Step 1 - Read The Module Material

Review:

- [concepts.md](concepts.md)
- [architecture.md](architecture.md)
- [Project 01 README](../../projects/project-01-model-api/README.md)

## Step 2 - List Providers

From the repository root:

```bash
python projects/project-01-model-api/app.py list-providers
```

Confirm that the client knows about multiple provider aliases without changing application code.

## Step 3 - Run A Successful Chat Call

```bash
python projects/project-01-model-api/app.py chat --provider acme-fast
```

Inspect the printed summary and the saved JSON report.

Questions to answer:

- Which layer loaded the prompt?
- Which layer selected the provider?
- Which part of the output would become metrics or trace attributes?

## Step 4 - Run A Failure Through The Same Interface

```bash
python projects/project-01-model-api/app.py chat --provider acme-rate-limited
```

The command should exit non-zero while still writing a JSON report.

Questions to answer:

- What fields stayed stable between success and failure?
- What changed?
- Why does a unified response shape help application teams?

## Step 5 - Optional Local HTTP API

Start the local API:

```bash
python projects/project-01-model-api/app.py serve
```

Then in another terminal send a request:

```bash
curl -X POST http://127.0.0.1:8000/api/chat -H "Content-Type: application/json" -d "{\"provider\":\"acme-fast\",\"message\":\"Explain stateless AI applications.\"}"
```

This shows how the same model client can sit behind an application API.

## Step 6 - Reflection

In your workbook, answer:

- What would you externalize before multiple teams used this application?
- What state, if any, is currently explicit?
- Where would asynchronous work appear if this application gained document ingestion?