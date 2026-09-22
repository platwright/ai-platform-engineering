# Chapter 08 - Human Feedback Integration

## The Role Of Human Feedback

Human feedback tells you that something went wrong, or right, in production. It is the signal closest to actual user experience. It is also noisy, incomplete, biased, and expensive to collect at scale.

Used well, human feedback:
- surfaces failure modes that automated evals miss
- provides raw material for growing the evaluation dataset
- gives product teams a quality signal that complements system metrics
- helps prioritize which parts of the system to improve next

Used poorly, human feedback becomes a dashboard that nobody acts on, or a source of false confidence when only happy users provide thumbs-up ratings.

## Types Of Feedback Signals

### Implicit Feedback

Inferred from user behavior without explicit rating:

- **Session abandonment**: user stops asking questions after a poor response
- **Query reformulation**: user rephrases the same question immediately (suggests the first response failed)
- **Conversation length**: short sessions after a response can indicate dissatisfaction
- **Copy events**: user copies the response text (typically a positive signal)

Implicit signals are noisy but can be collected at scale without user effort.

### Explicit Feedback

Directly solicited from the user:

- **Thumbs up / down**: binary quality signal, low friction
- **Rating scale**: 1–5 or 1–3, slightly more information
- **Free text feedback**: rich but expensive to collect and process
- **Correction**: user provides what the correct answer should have been

Explicit feedback is more reliable but suffers from response bias (users who bother to rate are not representative of all users).

## Feedback Collection Points

Not all feedback is equally valuable. The best collection points are:

- immediately after the model response, while the user can evaluate it
- at a natural pause in the conversation flow
- in-context within the product, not in a separate feedback form

For RAG systems, feedback should capture:

- was the response useful?
- was the response grounded in the retrieved context?
- was any retrieved content incorrect or outdated?

## The Feedback Pipeline

```
User provides feedback
        │
        ▼
Feedback Store
(indexed by session, response, model version, prompt version)
        │
        ├─── Low-quality responses ──→ Review Queue
        │                                    │
        │                             Human Reviewer
        │                                    │
        │                    ┌───────────────┼────────────────┐
        │                    ▼               ▼                ▼
        │              Root Cause       Add to Eval     Prompt Change
        │              Analysis         Dataset         PR Initiated
        │
        └─── High-quality responses ──→ Optional: add to eval dataset
                                         as positive examples
```

## Connecting Feedback To Evaluation Datasets

The most valuable use of human feedback is growing the evaluation dataset:

1. When a user flags a response as bad, a reviewer examines the full context
2. If the failure represents a recurring pattern, a new eval case is created
3. The eval case enters the eval dataset review process
4. After review, it is added to the dataset and tagged (e.g., `source: user-feedback-2025-09`)

This closes the loop: production failures become test cases that prevent the same failure from recurring.

## RLHF and DPO: The Platform Angle

Reinforcement Learning from Human Feedback (RLHF) and Direct Preference Optimization (DPO) use human preference data to fine-tune model weights. For platform engineers, the relevant questions are:

- **Data pipeline**: feedback data needs to flow from the product to a training dataset in a structured, auditable way
- **Privacy**: feedback may contain sensitive user content and needs the same data handling controls as production data
- **Data quality**: preference pairs need human review before they enter a fine-tuning dataset
- **Model lifecycle**: fine-tuned models need the same evaluation and deployment rigor as any model change

If your organization is fine-tuning models, human feedback is an input to the MLOps pipeline, not just an LLMOps concern.

## Privacy and Data Handling

Human feedback frequently contains sensitive content:

- user questions that reveal personal or organizational information
- feedback text that quotes problematic model outputs
- metadata that connects feedback to identifiable users

Before using feedback data for anything beyond immediate alerting:

- apply anonymization or pseudonymization
- enforce data retention limits
- confirm legal basis (GDPR, CCPA, etc.)
- store feedback with the same access controls as production data

A feedback pipeline that ignores privacy creates a secondary data leak risk separate from the primary AI system.

## Closing The Feedback Loop Visibly

Users who provide feedback feel heard when they see improvement. Even if the improvement is not directly connected to their specific feedback, communicating product quality improvements builds trust:

- release notes that mention evaluation score improvements
- in-product messages when a known issue is resolved
- transparency reports on system quality trends

This visible loop is operationally irrelevant but product-relevant. Platform engineers should make it possible even if the product team drives the communication.

## Feedback Metrics

Track these signals as platform health indicators:

| Metric | Interpretation |
|---|---|
| Negative feedback rate | % of responses with thumbs down |
| Feedback volume | Whether users engage with feedback at all |
| Feedback-to-fix cycle time | How long from negative feedback to production improvement |
| Cases added to eval from feedback | Rate at which production failures improve the eval suite |
