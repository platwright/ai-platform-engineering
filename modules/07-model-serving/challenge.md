# Module 07 Challenge

## Challenge Prompt

Acme AI wants to serve an open model internally for three use cases:

- low-volume development testing
- steady staging traffic
- production chat traffic with unpredictable spikes

Design the serving strategy.

## Deliverable

Create a note in:

- `my-solutions/module-07-serving-strategy.md`

Include:

1. model size and precision assumptions
2. single-node versus distributed serving choice
3. rollout and benchmarking plan
4. latency metrics you would set as early targets
5. fallback or degradation ideas if capacity is exhausted