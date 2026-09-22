# Module 12 Verification

## Check 1 - Layer Understanding

Without looking at the chapter, name the five observability layers for AI systems and give one concrete metric or signal for each.

## Check 2 - Token Logging

Verify that your application now logs token usage:

```bash
python applications/sample-rag/app.py query \
  --tenant team-a \
  --question "What is retrieval freshness?"
```

- [ ] Output includes `prompt_tokens` count
- [ ] Output includes `completion_tokens` count
- [ ] Output includes a latency measurement in ms
- [ ] You can explain why `prompt_tokens` is the number it is

## Check 3 - TTFT Awareness

Answer without looking at the chapter:

1. What specifically does TTFT measure?
2. Why is TTFT measured differently in streaming vs non-streaming responses?
3. Name two causes of high TTFT that are distinct from high total latency.

## Check 4 - Metrics Schema

Confirm your `eval/observability-design.yaml` includes:

- [ ] At least one counter metric with a tenant label
- [ ] At least one histogram metric with appropriate buckets for millisecond latency
- [ ] At least one metric for token usage
- [ ] At least one metric that would detect zero-result RAG queries

## Check 5 - Alert Design

Confirm your `eval/sample-alert.yaml`:

- [ ] Contains a valid Prometheus alerting rule format
- [ ] Has a `for` duration requirement (not instant-fire)
- [ ] Has a `runbook` annotation
- [ ] Uses a threshold that you can justify based on the chapter material

## Check 6 - Dashboard Design

You should be able to describe the top row of an AI platform dashboard in 60 seconds. What are the 4-5 most important panels and what does each show?

## Check 7 - Privacy Reasoning

Confirm you can explain:

- [ ] What privacy risk arises from logging full prompt and response text
- [ ] At least two mitigations for that risk
- [ ] What a "PII-scrubbed prompt preview" would look like for this use case
- [ ] How sampling affects both cost and privacy risk simultaneously

## Check 8 - Evaluation Observability Connection

Explain how the eval score metric from Module 11 connects to Module 12's observability layer:

- [ ] How does the eval runner write its score to a metric?
- [ ] How does that metric appear on the platform dashboard?
- [ ] What would a "quality SLO breach" alert look like in terms of Prometheus rule syntax?
