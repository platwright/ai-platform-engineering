# Module 11 Concepts

## Prompts Are Operational Artifacts

A prompt is not a string buried in source code. In a production AI system, a prompt is an operational artifact with a version, an author, an evaluation history, and a deployment status. When a prompt changes, production behavior changes. That change deserves the same review, testing, and rollback capability as any other release.

## The Core LLMOps Extension

MLOps covers training pipelines, model registries, feature stores, and deployment automation. LLMOps keeps all of that and adds the layer that generative AI requires:

- prompt versioning and registries
- evaluation against open-ended, non-deterministic outputs
- regression detection that tolerates variance while catching genuine degradation
- human feedback pipelines that close the loop from product behavior to improvement

## Non-Determinism Changes Testing Fundamentally

Classic ML models are evaluated with exact-match accuracy, F1, or AUC against labeled test sets. LLM outputs are open-ended. The same question asked twice produces different text, but both may be correct.

This means evaluation must:
- use rubrics, not just expected strings
- run multiple samples and reason statistically
- involve semantic similarity or LLM-as-judge scoring rather than string equality

## Evaluation Datasets Are As Important As The Model

A great model evaluated against a poor dataset produces misleading results. Evaluation datasets need careful design: coverage of real user behavior, edge cases, adversarial inputs, and regular maintenance as the product and data evolve.

## CI Gates For AI Must Be Cost-Aware

Running a full evaluation suite on every commit is expensive and slow. Tiering evaluation by change type (prompt change vs config change vs code refactor) keeps CI fast and affordable. Reserve deep evaluation for releases that touch the model or prompt.

## Human Feedback Is A Signal, Not A Solution

Thumbs up and thumbs down feedback from users tells you something is wrong. It does not tell you how to fix it, and it is subject to selection bias. Human feedback is most useful as a trigger for investigation and as raw material for building better evaluation datasets.
