# Chapter 03 - Prompt Registries and Management

## What A Prompt Registry Is

A prompt registry is a centralized service for storing, versioning, promoting, and auditing prompt templates. It does for prompts what a container registry does for images or what a model registry does for ML artifacts.

At minimum, a prompt registry provides:

- a storage location for versioned prompt files
- a promotion workflow (dev → staging → production)
- a query interface to retrieve a specific version by ID and version tag
- an audit log of who deployed what and when

At scale, it also provides:

- eval score history per version
- model compatibility metadata
- rollback mechanisms
- access control per prompt or per environment

## Why A Registry Differs From Git Storage

Git stores everything. A registry enforces a lifecycle.

With only Git, a developer can merge a prompt change directly to the main branch and it goes to production on the next deploy without any evaluation run. A registry makes deployment a separate, explicit step from merging. The pipeline must promote a version to staging, run evaluation, and then promote to production — the merge alone does not deploy.

## Promotion Workflow

```
Draft (dev branch)
     │
     ▼
dev registry  ──→  peer review  ──→  merge to main
                                          │
                                          ▼
                                    staging registry
                                          │
                                          ▼
                                    evaluation run
                                          │
                              ┌───────────┴────────────┐
                              ▼                        ▼
                         score ≥ threshold       score < threshold
                              │                        │
                              ▼                        ▼
                       production registry        investigation
```

## Metadata A Registry Should Track

| Field | Purpose |
|---|---|
| `id` | Stable identifier for this prompt (does not change across versions) |
| `version` | Semantic version string |
| `environment` | dev / staging / production |
| `model_pin` | Exact model version this prompt was validated against |
| `eval_dataset` | Eval dataset version used for scoring |
| `eval_score` | Score at time of promotion |
| `promoted_at` | Timestamp of promotion to this environment |
| `promoted_by` | Identity of promoter |
| `description` | Human-readable change summary |
| `rollback_target` | Previous production version this replaces |

## File-Based Registry (Simple)

A practical starting implementation uses a directory structure with a `registry.json` manifest:

```
prompts/
├── registry.json              ← index of all prompts and their current env status
├── rag-grounding/
│   ├── v1.3.0.yaml            ← previous production
│   └── v1.4.0.yaml            ← current production
└── chat-system/
    └── v2.0.0.yaml
```

`registry.json`:
```json
{
  "rag-grounding": {
    "production": "1.4.0",
    "staging": "1.5.0-rc",
    "dev": "1.5.1-draft"
  },
  "chat-system": {
    "production": "2.0.0",
    "staging": "2.0.0",
    "dev": "2.1.0-draft"
  }
}
```

A simple Python loader reads the registry and loads the correct version for the current environment:

```python
import json, yaml, os

def load_prompt(prompt_id: str, env: str = "production") -> dict:
    registry = json.load(open("prompts/registry.json"))
    version = registry[prompt_id][env]
    path = f"prompts/{prompt_id}/v{version}.yaml"
    return yaml.safe_load(open(path))
```

## Dedicated Registry Tools

When the file-based approach becomes limiting, dedicated tools offer more:

| Tool | What It Adds |
|---|---|
| LangSmith | UI for prompt management, eval integration, tracing |
| PromptLayer | Request logging, prompt version tracking, A/B testing |
| Weights & Biases Prompts | Eval tracking, comparison across versions |
| Promptfoo | CLI-based eval runner with prompt config format |
| Custom registry | Full control, integration with your existing secrets and CI tooling |

## Access Control

Prompt registries should enforce who can promote to production:

- developers can promote to dev and staging
- platform team or tech lead approval required for production
- automated promotion only after eval score threshold is met
- human override possible with explicit approval record

This mirrors the access model for production secrets and deployment pipelines.

## The Application Side

The application retrieves the current production prompt at startup or request time:

```python
# Load at startup (cached)
PROMPT = load_prompt("rag-grounding", env=os.getenv("APP_ENV", "production"))

# Use in request handler
def handle_rag_query(question: str, context: str) -> str:
    system = PROMPT["content"].format(context=context)
    return call_model(system=system, user=question, **PROMPT["parameters"])
```

This pattern means the prompt version deployed to production is explicit, auditable, and not embedded in application code.
