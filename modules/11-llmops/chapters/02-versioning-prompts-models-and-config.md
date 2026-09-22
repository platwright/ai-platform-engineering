# Chapter 02 - Versioning Prompts, Models, and Config

## Why Versioning Matters For LLM Systems

In conventional software, a code change goes through version control, review, and CI before it reaches production. That process creates an audit trail, enables rollback, and forces a review moment.

Prompts, model pins, and generation parameters all change production behavior just as much as code. When they are not versioned:

- no one knows what changed when behavior shifts
- rollback is manual and risky
- A/B testing is impossible
- debugging prompt regressions is guesswork

## What To Version

### Prompt Templates

Every prompt template that is executed in production should have a version. That includes:

- system prompts
- RAG grounding prompts
- few-shot example sets
- tool descriptions
- evaluation judge prompts

A minimal version record contains:

```json
{
  "id": "rag-grounding-prompt",
  "version": "1.4.0",
  "created_at": "2025-09-01T10:00:00Z",
  "author": "platform-team",
  "description": "Updated grounding instruction to reduce hallucination on factual questions",
  "model_compatibility": ["gpt-4o-mini", "llama-3.1-70b"],
  "eval_score": 0.88,
  "eval_dataset_version": "v3.1",
  "content": "You are a grounded assistant..."
}
```

### Model Pins

Always pin the specific model version used in production. Providers update models silently or with limited notice. A pin like `gpt-4o-2024-08-06` gives you a stable behavior anchor.

When a new model version is available:
1. run your evaluation suite against both versions
2. compare scores
3. promote the new version if the score is equal or better
4. document the comparison in the version record

### Generation Parameters

Parameters like `temperature`, `max_tokens`, `top_p`, and `stop` sequences are operational configuration. Store them alongside the prompt version they were validated with, not separately.

```yaml
# prompts/rag-grounding/v1.4.0.yaml
id: rag-grounding-prompt
version: 1.4.0
model: gpt-4o-mini-2024-07-18
parameters:
  temperature: 0.3
  max_tokens: 800
  top_p: 0.9
content: |
  You are a grounded assistant...
```

## Git-Based Prompt Management

The simplest approach: store prompts as files in the same repository as the code that uses them.

```
prompts/
├── rag-grounding/
│   ├── v1.3.0.yaml
│   ├── v1.4.0.yaml    ← current production
│   └── v1.5.0-dev.yaml
├── system-chat/
│   ├── v2.0.0.yaml
│   └── v2.1.0-rc.yaml
└── evaluation-judge/
    └── v1.0.0.yaml
```

Advantages: free, familiar, branch-based review workflow, change history in git log.

Limitations: no centralized dashboard, harder to search across versions, no built-in eval score tracking.

## Semantic Versioning For Prompts

Adopt a simple versioning convention:

- **Major** (`2.0.0`): completely rewritten prompt, behavior change expected
- **Minor** (`1.4.0`): new capability added, backward-compatible change
- **Patch** (`1.3.1`): minor wording fix, expected minimal behavior change

This mirrors software semantic versioning and gives reviewers immediate context about the risk level of a prompt change.

## Linking Versions Together

A complete version chain for a production deployment looks like:

```
Production Release 2025-09-15
├── prompt: rag-grounding v1.4.0
├── model: gpt-4o-mini-2024-07-18
├── parameters: temperature=0.3, max_tokens=800
├── eval dataset: rag-eval-v3.1
└── eval score: 0.88 pass rate (threshold: 0.80)
```

This chain is what makes a meaningful rollback possible: you are not just reverting a prompt, you are reverting to a validated, linked set of artifacts.

## Config Versioning

Application-level configuration that changes model behavior — RAG chunk count, reranker top-k, routing thresholds — should be treated the same as prompt versions. A config change without a corresponding eval run is a production change with no quality gate.

## Practical Starting Point

If your organization has no prompt versioning today, start here:

1. Create a `prompts/` directory in the application repository
2. Move all prompt strings from code into YAML files
3. Add a `version` and `description` field to each file
4. Require a PR review for any prompt file change
5. Add a note in the PR template: "If you changed a prompt, rerun the eval suite"

That is not a full LLMOps platform. It is a significant improvement over prompts embedded in code with no history.
