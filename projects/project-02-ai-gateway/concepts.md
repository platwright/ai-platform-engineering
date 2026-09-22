# Project 02 Concepts

## The Serving Stack

Project 02 is about the serving path itself, not only the application calling it.

The serving path includes:

- model weights
- model runtime
- inference API
- Kubernetes deployment
- client-side load generation
- report interpretation

## Why OpenAI-Compatible APIs Matter

An OpenAI-compatible API surface is useful because it gives a stable interface across different model-serving backends. That makes benchmarking, application integration, and migration easier.

## Why Benchmarking Starts Early

You do not need a full observability platform to begin reasoning about latency and throughput. A basic benchmark can already tell you:

- how long requests take
- what throughput you can sustain
- what token usage looks like
- where failure rates appear

## What This Project Intentionally Does Not Do

This project does not pretend to be a full production load-testing platform. It is a course artifact that teaches the shape of performance validation and a Kubernetes-native serving setup.