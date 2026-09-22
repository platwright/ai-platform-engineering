# Chapter 1.2 - Training vs Inference

## The Core Difference

Training creates or updates a model. Inference uses a model that already exists.

That sounds simple, but operationally it is one of the most important distinctions in the entire course.

## Training Flow

```text
Dataset
  -> training job
  -> compute cluster
  -> checkpoints
  -> model artifact
```

Training is usually:

- long running
- throughput oriented
- expensive in compute and storage
- tolerant of batch workflows
- artifact heavy

## Inference Flow

```text
Request
  -> model runtime
  -> output or tokens
```

Inference is usually:

- latency sensitive
- user or application facing
- dependent on concurrency and queueing behavior
- sensitive to prompt length and output length
- easier to consume than to operate at scale

## Infrastructure Differences

| Topic | Training | Inference |
| --- | --- | --- |
| Main goal | produce a model artifact | serve predictions or generations |
| Typical duration | minutes to days | milliseconds to seconds or longer for streaming |
| Scheduling pattern | jobs and pipelines | services and APIs |
| Data pattern | large dataset scans | per-request inputs |
| Storage pattern | datasets, checkpoints, artifacts | model weights, caches, logs, traces |
| Performance focus | throughput and completion | latency, concurrency, and cost per request |

## Why This Matters To Platform Engineers

If you confuse training and inference, you will misdesign:

- autoscaling rules
- storage strategy
- network policy
- failure handling
- observability
- cost expectations

For example, retries in inference can multiply user-facing cost quickly. Retries in training affect wall-clock time and cluster usage differently.

## CPU, GPU, Storage, And Network Implications

Training often pushes hard on:

- distributed compute
- high-throughput storage
- checkpoint persistence
- interconnect bandwidth

Inference often pushes hard on:

- request concurrency
- model load times
- memory footprint
- prompt and output token processing
- network paths for user and service traffic

## Failure Modes

Training failures often look like:

- failed jobs
- checkpoint corruption
- out-of-memory crashes during training steps
- long pipeline delays

Inference failures often look like:

- slow responses
- timeouts
- provider errors
- bad generations
- rate limits
- overloaded model servers

## The Practical Rule

In most organizations, many more engineers will consume inference than operate training. That is why AI platform engineering often begins with inference systems, even when the company never trains a foundation model from scratch.