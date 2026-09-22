# Chapter 05 - Automated Evaluation Patterns

## Why Automated Evaluation Is Hard

Evaluating classification models is straightforward: compare predicted labels to ground truth labels and compute accuracy, precision, recall, or F1. For open-ended LLM outputs, there is no single ground truth. A question about retrieval freshness might have ten correct answers with different levels of detail and different correct emphasis.

Automated evaluation for LLMs must approximate the judgment of a domain-aware human reviewer, quickly and at low cost.

## Pattern 1: Exact Match

Compare the model output directly to an expected string.

```python
def exact_match(actual: str, expected: str) -> float:
    return 1.0 if actual.strip() == expected.strip() else 0.0
```

**When it works**: classification tasks, structured output extraction, well-defined factual lookups where one answer is clearly correct.

**When it fails**: any open-ended generation, summarization, conversational responses, or questions with multiple valid phrasings.

Use exact match as a sanity check for structured output pipelines, not as a general quality signal.

## Pattern 2: Keyword and Theme Presence

Check whether expected concepts or keywords appear in the response.

```python
def keyword_score(response: str, expected_themes: list[str]) -> float:
    response_lower = response.lower()
    matched = sum(1 for theme in expected_themes if theme.lower() in response_lower)
    return matched / len(expected_themes)
```

**When it works**: validating that responses address required concepts; low-cost smoke tests.

**When it fails**: surface-level — a response that contains all the keywords in the wrong context or with incorrect claims still scores well.

## Pattern 3: Semantic Similarity

Compute the embedding of the response and the expected answer, then measure cosine similarity.

```python
def semantic_similarity(response: str, reference: str, embed_fn) -> float:
    v1 = embed_fn(response)
    v2 = embed_fn(reference)
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = sum(a ** 2 for a in v1) ** 0.5
    norm2 = sum(b ** 2 for b in v2) ** 0.5
    return dot / (norm1 * norm2)
```

**When it works**: comparing responses to reference answers when phrasing varies; catching semantically correct responses that use different vocabulary.

**When it fails**: responses that are semantically close but factually wrong; very short responses with high cosine similarity to reference through coincidence.

## Pattern 4: LLM-as-Judge

Use a separate LLM to evaluate the quality of the response against a rubric or the question. This is the most powerful and flexible pattern.

```python
JUDGE_PROMPT = """
You are an expert evaluator. Given a question and a model response, score the response 
from 0 to 3 on each criterion:

Question: {question}
Response: {response}

Criteria:
1. Accuracy: Is the response factually correct based on the provided context?
2. Completeness: Does the response address all important aspects of the question?
3. Grounding: Is the response grounded in the retrieved context rather than fabricated?

Return JSON: {{"accuracy": 0-3, "completeness": 0-3, "grounding": 0-3, "reasoning": "..."}}
"""
```

**When it works**: open-ended generation, rubric-based evaluation, nuanced quality assessment at scale.

**When it fails**: the judge model has the same biases as the model under test; the judge can be inconsistent; judge hallucinations affect scores; costs more than simple methods.

**Judge model selection**: use a different, stronger model than the model being evaluated when possible. Do not use the same model to evaluate itself.

## Pattern 5: Composite Scoring

Combine multiple patterns into a single weighted score:

```python
def composite_score(
    response: str,
    question: str,
    expected_themes: list[str],
    reference: str,
    judge_fn
) -> dict:
    kw = keyword_score(response, expected_themes)
    judge = judge_fn(question, response)
    combined = 0.3 * kw + 0.7 * (judge["accuracy"] / 3)
    return {"keyword": kw, "judge": judge, "composite": combined}
```

Weights should be calibrated against human evaluation on a held-out validation set.

## Scoring Aggregation

Individual case scores aggregate into a report:

```python
{
  "eval_run_id": "eval-2025-09-01-14:32",
  "prompt_version": "rag-grounding-v1.4.0",
  "model": "gpt-4o-mini-2024-07-18",
  "dataset_version": "rag-eval-v3.1",
  "total_cases": 200,
  "passed": 174,
  "pass_rate": 0.87,
  "mean_composite_score": 0.82,
  "low_scoring_cases": ["eval-031", "eval-076", "eval-142"],
  "categories": {
    "core": {"pass_rate": 0.91},
    "edge": {"pass_rate": 0.80},
    "adversarial": {"pass_rate": 0.78}
  }
}
```

## Calibration

Automated scores are useful only if they correlate with human judgment. Periodically run a calibration exercise:

1. Have humans score a sample of 50–100 cases
2. Compare automated scores to human scores
3. Adjust weights or rubrics where automated scores consistently disagree with humans

A well-calibrated LLM judge should achieve Spearman correlation ≥ 0.7 with human judgment on the calibration set.

## Cost Management

Evaluation costs real money, especially with LLM-as-judge:

| Pattern | Relative Cost | Speed |
|---|---|---|
| Exact match | Negligible | Instant |
| Keyword presence | Negligible | Instant |
| Semantic similarity | Low (embed only) | Fast |
| LLM-as-judge | High (2 LLM calls per case) | Slow |

Tier your evaluation:
- **Pre-merge smoke test**: keyword + semantic, 10-20 cases, runs in seconds
- **CI merge gate**: composite scoring, 100-200 cases, 5-10 minutes
- **Release gate**: LLM-as-judge, full dataset, 30-60 minutes
