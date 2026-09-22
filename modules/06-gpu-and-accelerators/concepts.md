# Module 06 Concepts

## Why Accelerators Matter

Modern LLM and deep learning inference workloads perform large amounts of parallel numeric computation. GPUs and other accelerators are designed to handle that kind of work far more efficiently than general-purpose CPUs in many scenarios.

## The Constraint Is Not Only Compute

For platform engineers, the first hard limit is often memory, not raw compute. Model weights, activations, and KV cache all compete for accelerator memory.

## Accelerator Planning Is A Platform Problem

Once a service needs accelerators, platform design changes:

- scheduling becomes stricter
- node pools become specialized
- utilization gets more expensive to waste
- observability has to include hardware metrics

## Sharing Changes The Tradeoff

Accelerators are expensive, which makes sharing attractive. But sharing can reduce isolation and make performance behavior harder to predict. That is why concepts like time slicing, MIG, and fractional access matter.

## Kubernetes Adds Placement And Policy

GPU usage on Kubernetes is not only about requesting `nvidia.com/gpu`. It also involves:

- device plugins or newer allocation mechanisms
- node labeling and taints
- environment separation
- capacity strategy

## What This Module Tries To Teach

The objective is not to memorize hardware internals. It is to make infrastructure choices around accelerators technically defensible.