# Module 08 Concepts

## Why A Gateway Exists

As soon as multiple applications, providers, or model policies exist, a shared model access layer becomes valuable. A gateway provides that layer.

## The Gateway Is A Control Point

An AI gateway can centralize:

- routing
- fallback
- credentials and provider access
- rate limiting
- usage tracking
- caching
- policy hooks

## Unified Endpoints Reduce Cognitive Load

Applications prefer one stable endpoint. The gateway can then hide provider-specific transport and expose a governed interface.

## Routing Is A Policy Decision

Cheap model for simple requests. More reliable or private route for sensitive requests. Fallback path when the primary fails. Those are platform decisions, not only application details.

## Caching Is A Tradeoff

Prompt caching can reduce cost and latency for repeated requests. Semantic caching can go further, but it increases correctness risk because similar is not identical.

## Metrics Matter

Without usage and policy metrics, a gateway becomes a black box. Good gateways make routing decisions visible.