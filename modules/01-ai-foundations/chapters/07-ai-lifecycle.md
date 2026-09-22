# Chapter 1.7 - AI Lifecycle

## Why Lifecycle Thinking Matters

AI systems are not stable because a single prompt worked once. They become stable when the full lifecycle is controlled.

This course uses the following lifecycle model:

```text
Experiment
  -> Develop
  -> Evaluate
  -> Package
  -> Deploy
  -> Serve
  -> Observe
  -> Improve
```

## Experiment

Teams test ideas, prompts, data, and model choices. This stage is fast and exploratory, but it should still leave evidence behind.

Useful artifacts:

- prompts
- sample datasets
- notes on outcomes
- evaluation criteria

## Develop

The idea becomes a repeatable application or workflow.

Useful artifacts:

- code
- configuration
- prompt templates
- dependency definitions

## Evaluate

This stage asks whether the system is actually good enough. Ordinary unit tests are not enough.

Evaluation may include:

- correctness
- groundedness
- latency
- cost
- safety or policy checks

## Package

Now the system becomes deployable.

Useful artifacts:

- container images
- model references
- deployment config
- environment templates

## Deploy

The packaged system is rolled out into an environment with change control and rollback expectations.

## Serve

The system begins handling traffic. This is where platform design becomes visible to end users through latency, reliability, and cost.

## Observe

You should capture enough telemetry to answer:

- what changed
- what failed
- how much it cost
- what the user experienced

## Improve

Improvements should be deliberate rather than ad hoc. That means prompt revisions, model changes, retrieval changes, and deployment changes should all be observable and comparable.

## Where This Module's Mini-Project Fits

The observer project lives near the beginning of the lifecycle. It is a small but concrete example of how even the first inference call should produce artifacts and telemetry worth keeping.

## Platform Takeaway

Production AI work is a loop. The platform exists to make each loop faster, safer, and more repeatable for application teams.