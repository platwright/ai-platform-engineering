# Module 01 Lab

## Goal

Use the mini-project to observe an AI inference interaction the way a platform engineer would: measure latency, inspect token usage, capture the response payload, and see how errors are represented.

## Outcome

By the end of this lab, you should have:

- run the observer in mock mode successfully
- generated a JSON report artifact
- inspected one successful response and one failure response
- written a short note about what fields would matter in production telemetry

## Step 1 - Read The Module Narrative

Work through the module chapters in order before you run the project. The commands are simple, but the point of the exercise is to connect the output to workload behavior.

Start here:

- [concepts.md](concepts.md)
- [architecture.md](architecture.md)
- [project/README.md](project/README.md)

## Step 2 - Run The Mock Success Path

From the repository root:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock
```

This uses the bundled success fixture and writes a JSON report in `modules/01-ai-foundations/project/runs/`.

## Step 3 - Inspect The Report

Open the generated JSON report and identify:

- status code
- latency in milliseconds
- prompt token count
- completion token count
- total token count
- finish reason
- response text

Then write one short note in your workbook describing why each field matters operationally.

## Step 4 - Run The Mock Failure Path

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock --mock-file modules/01-ai-foundations/project/fixtures/mock-rate-limit.json
```

This should exit non-zero and write a report that captures the error.

## Step 5 - Optional Hosted API Path

If you have access to an OpenAI-compatible chat endpoint, set these environment variables in your shell:

- `MODEL_API_URL`
- `MODEL_API_KEY`
- `MODEL_NAME`

Then run:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode http
```

## Step 6 - Compare Results

Write down:

- which fields were stable between success and failure runs
- which fields changed when the request failed
- what you would turn into metrics, traces, and logs in a real platform

## Step 7 - Record Your Reflection

In your workbook, answer:

- Why does this small script already show the need for observability?
- Which difference between training and inference feels most operationally important to you?
- What extra metadata would you capture before letting multiple teams use this endpoint?