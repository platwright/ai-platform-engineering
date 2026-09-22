# Chapter 07 - Environment Cost Controls

## The Dev and Staging Cost Problem

Development and staging environments are necessary. They are also the most common source of AI cost waste because:

- developers test prompts interactively, often with no token limit
- automated CI evaluation runs may use expensive models when cheap models would suffice
- staging environments may run 24/7 with GPU instances that are idle most of the time
- experiments use frontier models by default because they are convenient, not because they are needed

In production, costs are justified by user value. In dev and staging, most costs produce no direct user value.

## Environment-Level Model Tiers

Configure dev and staging to use cheaper model tiers by default:

```python
DEFAULT_MODEL_BY_ENV = {
    "production": "gpt-4o-mini",    # cheap, production quality
    "staging":    "gpt-4o-mini",    # same as production for eval accuracy
    "development": "gpt-4o-mini",   # cheap, override available
    "ci":         "gpt-4o-mini",    # batch API where possible
}

def get_model(requested: str | None, env: str) -> str:
    if requested:
        return requested  # explicit override
    return DEFAULT_MODEL_BY_ENV.get(env, "gpt-4o-mini")
```

Developers who genuinely need a frontier model for a test can explicitly request it, but the default is always the cheap tier.

## Per-Environment Token Quotas

Set hard limits on token spending per environment:

```python
MONTHLY_TOKEN_BUDGET = {
    "production": float("inf"),   # no hard limit; alert-based management
    "staging":    10_000_000,     # 10M tokens/month
    "development": 1_000_000,     # 1M tokens/month per developer
    "ci":          5_000_000,     # 5M tokens/month for CI runs
}
```

When a quota is approached, send a warning. When it is reached, block requests until reset:

```python
def check_quota(tenant: str, env: str, tokens_requested: int) -> bool:
    usage = get_monthly_usage(tenant, env)
    budget = get_budget(tenant, env)
    if usage + tokens_requested > budget:
        log_metric("quota_exceeded", {"tenant": tenant, "env": env})
        return False
    return True
```

## CI Evaluation Cost Management

Evaluation runs in CI use real model calls and cost real money. Strategies to reduce CI eval cost:

### Use Batch APIs

OpenAI and Anthropic batch APIs reduce cost by 50% for non-time-sensitive requests:

```python
# Instead of sending eval cases one at a time
for case in eval_dataset:
    response = call_model(case["question"])

# Use batch API (results available within 24 hours)
batch = create_batch_request(eval_dataset)
submit_batch(batch)
# ... wait for results ...
```

For overnight or weekly full eval runs, batch APIs save 50% on eval model costs.

### Tiered Eval Models

Use a cheap model for the initial scoring pass and a stronger model only for borderline cases:

```python
def tiered_eval(question: str, response: str) -> dict:
    # Fast cheap pass
    quick_score = score_with_model("gpt-4o-mini", question, response)
    if quick_score > 2.5 or quick_score < 1.0:
        return {"score": quick_score, "tier": "quick"}
    
    # Only borderline cases go to the expensive model
    full_score = score_with_model("gpt-4o", question, response)
    return {"score": full_score, "tier": "full"}
```

## Dev Environment Scheduled Shutdown

GPU instances in dev/staging environments should not run 24/7:

```yaml
# Kubernetes CronJob to scale down dev serving at end of day
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dev-serving-shutdown
spec:
  schedule: "0 20 * * 1-5"  # 8 PM weekdays
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: scaler
              image: bitnami/kubectl
              command:
                - kubectl
                - scale
                - deployment/vllm-dev
                - --replicas=0
                - -n
                - model-serving-dev
```

A development GPU instance running at idle during nights and weekends wastes approximately 60–70% of its monthly cost.

## Cost Sandbox for Experiments

Create a separate cost envelope for experimental or prototype work:

- separate Kubernetes namespace with separate GPU quota
- monthly budget cap on the experiment namespace
- automatic expiry of resources older than N days

This prevents experimental work from affecting production budgets or consuming shared infrastructure unexpectedly.
