# Chapter 06 - Model Selection and Cost Tradeoffs

## The Quality-Cost Frontier

Every model sits on a quality-cost frontier. The cost of a model API call is a function of its price per token. The quality is a function of its capability on your specific tasks.

The platform engineering question is: what is the cheapest model that meets the quality SLO for each use case?

## Capability Does Not Scale Linearly With Cost

A model that costs 10× more than a cheaper model does not produce 10× better outputs. The quality difference between tiers varies dramatically by task:

| Task Type | Quality Difference (expensive vs cheap) |
|---|---|
| Simple Q&A, factual lookup | Minimal — cheap models often match |
| Classification, routing | Minimal — often fine-tuned small models are best |
| Complex reasoning, multi-step | Significant — frontier models excel |
| Code generation (complex) | Significant for complex architecture tasks |
| Creative writing | Moderate — depends heavily on the style |
| RAG grounded response | Moderate — if context quality is good, cheap models are fine |

## Evaluating Model Tiers

The correct approach: run your evaluation suite on each candidate model and compare scores.

```python
# Run eval across two model tiers
for model in ["gpt-4o-mini", "gpt-4o"]:
    results = run_eval(
        dataset="eval/datasets/rag-eval-v3.1.json",
        model=model
    )
    print(f"{model}: pass_rate={results['pass_rate']:.2f}, "
          f"mean_score={results['mean_score']:.2f}")

# gpt-4o-mini: pass_rate=0.84, mean_score=0.79
# gpt-4o:      pass_rate=0.89, mean_score=0.84
# SLO threshold: 0.80 pass rate

# Result: gpt-4o-mini meets the SLO at 1/10th the cost
```

If the cheap model meets the SLO, the expensive model provides no value worth its cost difference.

## Fine-Tuning for Cost Reduction

Fine-tuning a small base model on domain-specific data can match a large frontier model's performance for a specific task at dramatically lower cost:

- **Fine-tuned 7B model**: may match GPT-4o on a narrow classification task
- **Inference cost**: 10–50× cheaper per token than GPT-4o
- **Tradeoff**: requires training data, training infrastructure, and maintenance

Fine-tuning is cost-effective when:
- the task is well-defined and has clear examples
- the volume is high enough to justify training cost
- the domain is specific enough that a general frontier model over-engineers the solution

## Open-Weight Models for Cost Reduction

Open-weight models (Llama, Mistral, Qwen, Gemma) can serve many tasks at dramatically lower per-token cost than proprietary APIs when self-hosted:

```
Cost comparison for a 1B token/month workload:
  GPT-4o mini:        ~$150/month
  Self-hosted Llama 8B: ~$30-50/month (2× A10G reserved)
  Self-hosted Llama 70B: ~$100-150/month (4× A10G reserved)
```

Open-weight models require operational overhead. The cost comparison must include:
- GPU instance reservation cost
- Operations engineering time (~0.5–1 FTE for model management)
- Monitoring and incident response infrastructure

## Routing By Task Type

Different features in an application can use different model tiers:

```python
TASK_MODEL_MAP = {
    "intent_classification":     "gpt-4o-mini",   # cheap, fast
    "entity_extraction":         "gpt-4o-mini",   # cheap, structured output
    "rag_grounded_answer":       "gpt-4o-mini",   # cheap if context is good
    "complex_analysis":          "gpt-4o",         # expensive but needed
    "code_review":               "gpt-4o",         # benefits from frontier
    "evaluation_judge":          "gpt-4o",         # judge needs to be strong
}
```

This per-task routing captures most of the cost savings of cheap models while preserving frontier model quality where it matters.

## Costs Over Time

Model pricing generally trends downward, but at uneven rates. The price of GPT-4-level capability has fallen by approximately 10× over three years. Planning model costs as fixed is a mistake.

Build into your FinOps review:
- quarterly review of model pricing
- re-evaluation of routing thresholds when new models are released
- benchmark new model versions as they release to identify upgrade opportunities
