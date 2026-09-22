# Module 03 Verification

Use this checklist before moving on.

## Reading Check

You should have completed all five chapter files and reviewed:

- [concepts.md](concepts.md)
- [architecture.md](architecture.md)
- [Project 01 README](../../projects/project-01-model-api/README.md)

## Project Check

List the providers:

```bash
python projects/project-01-model-api/app.py list-providers
```

Run a success path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-fast
```

Expected result:

- exit code `0`
- summary output with provider, status, latency, and response preview
- a new JSON report under `projects/project-01-model-api/runs/`

Run a failure path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-rate-limited
```

Expected result:

- non-zero exit code
- a saved JSON report
- a normalized error object in the report

## Understanding Check

You should be able to explain:

- the layers inside a typical AI application
- where state should and should not live
- why synchronous and asynchronous paths need different architecture
- which settings belong in configuration
- how twelve-factor principles adapt to AI applications
- why Project 01 is a precursor to a later AI gateway

## Exit Criteria

You are ready to move on when:

- Project 01 works in mock mode
- you can describe the architecture boundaries in your own words
- you can point to the places in Project 01 where prompt handling, config, and provider transport are separated