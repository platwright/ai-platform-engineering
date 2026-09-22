# Project 01 Verification

## Required Checks

List providers:

```bash
python projects/project-01-model-api/app.py list-providers
```

Expected result:

- provider aliases are listed
- the default provider is marked

Run a success path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-fast
```

Expected result:

- exit code `0`
- summary output including provider, status, latency, and response preview
- a saved JSON report

Run a failure path:

```bash
python projects/project-01-model-api/app.py chat --provider acme-rate-limited
```

Expected result:

- non-zero exit code
- saved JSON report
- normalized error object in the report

Optional compile check:

```bash
python -m py_compile projects/project-01-model-api/app.py projects/project-01-model-api/unified_model_client/*.py
```