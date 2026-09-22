# Module 04 Solution

## Expected Outcome

A correct completion shows that you can package the application and model API separately, run them together in Compose, and explain why the separation matters.

## Compose Stack Interpretation

The stack is intentionally small:

- `sample-chat` is the application-facing layer
- `model-api` is the model access layer
- Redis and Qdrant are early backing-service placeholders
- the observability service is there to make future stack expansion visible

## OOM Lab Interpretation

The OOM lab is successful when you can connect the failure to the configured memory limit instead of treating it as a random crash.

The important lesson is not only that memory is finite. It is that resource policy is part of workload design.