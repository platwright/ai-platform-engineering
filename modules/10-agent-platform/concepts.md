# Module 10 Concepts

## What An Agent Is

An agent is not only a model response. In platform terms, an agent usually combines:

- a model
- a control loop
- tools
- state or memory
- policy and safety controls

## Tool Execution Is The Risk Boundary

As soon as an agent can do something instead of only say something, tool execution becomes the central platform concern.

## State Makes Agents Harder To Operate

Agents often need state for tasks, memory, or workflow progress. That means operators must reason about persistence, privacy, replay, and cleanup.

## MCP Matters Because Discovery Matters

MCP is useful to platform engineers because it frames tools and resources as discoverable, governable surfaces rather than hidden application internals.

## Approval Is A Platform Feature

Human approval for risky operations should not be treated as a patch after an incident. It is a first-class runtime control.