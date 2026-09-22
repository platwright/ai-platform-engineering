# Project 02 Solution

## Expected Outcome

A correct completion shows that you can describe the model-serving stack, render the Kubernetes manifests, and produce a basic performance report from an OpenAI-compatible endpoint.

## What The Benchmark Should Show

Even the mock path should give you:

- request-level success and failure accounting
- latency percentile calculations
- simple throughput approximations
- an artifact you can compare across runs

## What It Does Not Yet Show

It does not replace server-side tracing, GPU metrics, or deep concurrency analysis. Those become important in later modules.