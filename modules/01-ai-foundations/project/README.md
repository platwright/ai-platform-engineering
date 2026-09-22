# Mini Project - AI Workload Observer

## Goal

Call an AI endpoint and record the result like a platform engineer would. The script captures:

- latency
- status code
- model metadata
- token usage
- response text
- error details

The project defaults to mock mode so you can run it without API keys. If you have access to an OpenAI-compatible chat endpoint, you can also run it against a real service.

## Files

- `ai_workload_observer.py`: the CLI script
- `prompts/foundation-check.txt`: default prompt for the request
- `fixtures/mock-success.json`: a successful mock response
- `fixtures/mock-rate-limit.json`: a failure fixture for rate-limit behavior
- `runs/`: generated JSON reports

## What This Teaches

This is a small project, but it already demonstrates important platform ideas:

- inference is an observable workload, not just an API call
- token usage and latency belong in runtime telemetry
- failures should still generate artifacts for diagnosis
- provider-specific APIs are better hidden behind stable interfaces later

## Run In Mock Mode

From the repository root:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock
```

This writes a JSON report into `modules/01-ai-foundations/project/runs/`.

## Simulate A Failure

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock --mock-file modules/01-ai-foundations/project/fixtures/mock-rate-limit.json
```

This should exit non-zero and still write a report.

## Run Against A Real Endpoint

Set these environment variables in your shell:

- `MODEL_API_URL`: full URL of an OpenAI-compatible chat completions endpoint
- `MODEL_API_KEY`: bearer token for the endpoint
- `MODEL_NAME`: model identifier to request

Then run:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode http
```

Example endpoint shape:

```text
https://api.openai.com/v1/chat/completions
```

## Example Output Fields

The generated JSON report includes fields such as:

- `timestamp_utc`
- `mode`
- `request`
- `response.status_code`
- `response.latency_ms`
- `response.usage`
- `response.finish_reason`
- `response.text`
- `response.error`

## Notes

- Generated JSON files under `runs/` are ignored by Git.
- Treat prompts and responses as potentially sensitive data in real environments.
- The script uses the Python standard library only, so no extra package install is required.