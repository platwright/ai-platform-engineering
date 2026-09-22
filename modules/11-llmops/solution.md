# Module 11 Solution

## Expected Eval Script Behavior

A successful eval run against the smoke dataset should produce output similar to:

```
[PASS] eval-001: score=0.75
[PASS] eval-002: score=1.00
[PASS] eval-003: score=0.50
[FAIL] eval-004: score=0.40
[PASS] eval-005: score=0.75

Results: 4/5 passed (80.0%)
Threshold: 60.0%
OVERALL: PASS
```

`eval-004` (operational signals) may score lower because the sample documents may not contain the operational vocabulary expected by the keyword scorer. This is a realistic finding — it means either the eval case needs refinement or the RAG pipeline needs better coverage of operational content.

## Prompt Registry Reference Design

Minimal file structure:

```
prompts/
├── registry.json
├── rag-grounding/
│   ├── v1.0.0.yaml
│   └── v1.1.0.yaml
└── chat-system/
    └── v1.0.0.yaml
```

`registry.json`:
```json
{
  "rag-grounding": {
    "production": "1.0.0",
    "staging": "1.1.0",
    "dev": null
  }
}
```

`rag-grounding/v1.0.0.yaml`:
```yaml
id: rag-grounding
version: 1.0.0
created_at: "2025-09-01T00:00:00Z"
author: platform-team
model: gpt-4o-mini-2024-07-18
parameters:
  temperature: 0.3
  max_tokens: 800
eval_score: 0.80
eval_dataset: rag-eval-v1.0
description: Initial grounding prompt for RAG platform
content: |
  You are a grounded assistant. Answer using only the provided context.
  If the answer is not in the context, say so clearly.
  
  Context:
  {context}
```

## Regression Simulation Reference

When you simplify the system prompt from:
```
You are a grounded assistant. Answer using only the provided context...
```

to:
```
Answer the question.
```

Expected behavior: the model starts generating responses from its training data rather than the retrieved context. Keyword coverage on themes like "freshness", "platform", and "multi-tenant" drops because the model generates generic responses that don't reflect the specific documents in the index.

The pass rate on the smoke dataset should drop to 0.40-0.60 depending on how much the prompt change affects each case.

## CI Pipeline Reference Implementation

The minimum CI workflow for prompt changes (see [Chapter 07](chapters/07-ai-cicd-pipelines.md)):

```yaml
name: Prompt Eval
on:
  pull_request:
    paths: ['prompts/**']

jobs:
  smoke-eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: |
          python eval/run_eval.py \
            --dataset eval/datasets/rag-smoke.json \
            --service-name team-a-kb \
            --threshold 0.60
        env:
          MODEL_API_URL: ${{ secrets.STAGING_MODEL_API_URL }}
          MODEL_API_KEY: ${{ secrets.STAGING_MODEL_API_KEY }}
```

This is intentionally minimal. A production pipeline would add staging environment setup, full eval on merge, artifact archiving, and PR comments with score summaries.

## LLM-as-Judge Reference Prompt

```python
JUDGE_PROMPT = """You are an expert evaluator for a RAG (Retrieval-Augmented Generation) system.

Given a question and a model response, score the response on three criteria from 0 to 3:

Question: {question}
Response: {response}

Scoring:
- groundedness (0-3): Is the response grounded in retrieved facts? (3=fully grounded, 0=fabricated)
- completeness (0-3): Does the response address the full question? (3=complete, 0=incomplete)
- relevance (0-3): Is the response directly relevant to what was asked? (3=highly relevant, 0=off-topic)

Return only JSON: {{"groundedness": N, "completeness": N, "relevance": N, "reasoning": "one sentence"}}"""
```

The composite score weight of 70% judge / 30% keyword reflects that rubric evaluation is more reliable than keyword matching for RAG quality, but keyword coverage provides a fast, cheap sanity check.
