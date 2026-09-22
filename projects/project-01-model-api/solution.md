# Project 01 Solution

## What A Correct Project Should Demonstrate

- one application-facing entry point can reach multiple provider backends
- prompts, request defaults, and provider settings can live in explicit config or files
- application code does not need to parse every provider schema separately
- failures still produce usable artifacts for troubleshooting

## Expected Provider Story

The mock providers should let you validate:

- a faster success path
- a second success path with different latency and content
- a failure path that still returns a normalized error record

The optional OpenAI-compatible path proves that the same application abstraction can reach a real provider when configuration and credentials are present.