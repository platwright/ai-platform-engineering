# Module 04 Concepts

## Why Containers Matter Here

Containerization is the first time the course turns application architecture into runtime packaging. Once the application becomes an image, platform concerns become concrete:

- what gets shipped together
- what stays external
- how configuration enters the process
- how services talk to each other
- how resource limits are enforced

## Split The Runtime By Responsibility

This module uses two images on purpose:

- the sample chat application image
- the Project 01 model API image

That split keeps the application layer and model access layer separate while still letting them run together as one stack.

## Application Images And Model Images Are Different

An application image usually contains:

- application code
- configuration templates
- prompt assets
- runtime entry point

A model image or model-serving image may contain:

- runtime server
- model loading logic
- optional model weights or references
- inference-specific configuration

Those are different concerns, and they should not automatically be merged.

## Containers Make Boundaries Visible

Once the application is in a container, hidden assumptions become obvious:

- file paths
- local hostnames
- config injection
- port usage
- health endpoints
- memory limits

## Local Stacks Are A Learning Tool

Docker Compose is useful because it makes service boundaries, network connections, and backing services visible without requiring a cluster. It is the right local-first bridge before Kubernetes.

## Failure Labs Matter Early

Container OOM failures are a good example of platform thinking. The failure is not random. It is a concrete interaction between workload behavior and resource policy.