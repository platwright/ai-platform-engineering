# Module 02 Lab

## Goal

Send LLM requests with different configurations, observe how parameters affect output, and build familiarity with the request/response protocol before connecting to live models in later modules.

## Prerequisites

- Project 01 running locally (provides the model API abstraction)
- A working Python environment

## Step 1 - Observe Token Usage

Send a basic request through Project 01 and note the token usage fields in the JSON run artifact:

```bash
python projects/project-01-model-api/app.py chat \
  --provider acme-fast \
  --message "Explain what a context window is in one sentence."
```

Open the generated run artifact in `projects/project-01-model-api/runs/` and locate:

```json
{
  "usage": {
    "prompt_tokens": ...,
    "completion_tokens": ...,
    "total_tokens": ...
  }
}
```

Write down the token counts. How do they compare to the word count of the prompt?

## Step 2 - Observe the Request Structure

Open `projects/project-01-model-api/app.py` or the provider adapter code and find where the chat request is built. Identify:

- how the system prompt contributes tokens
- where `max_tokens` is set
- whether `temperature` is configured

Note what defaults are applied. Are they documented?

## Step 3 - Compare Short and Long System Prompts

Modify the application configuration to try two system prompt variants:

**Short variant** (in `projects/project-01-model-api/config/app.example.json`):
```json
{ "system_prompt": "You are a helpful assistant." }
```

**Long variant**:
```json
{ "system_prompt": "You are a senior platform engineer assistant with expertise in AI infrastructure, Kubernetes, model serving, retrieval systems, agent architecture, observability, security, and cost management. You provide precise, technically accurate answers grounded in real production experience. You avoid vague generalities and always connect concepts to operational implications." }
```

Run the same user message with both variants and compare token counts in the run artifacts. What is the difference in `prompt_tokens`?

## Step 4 - Simulate a Structured Output Request

Inspect the mock provider fixtures in `projects/project-01-model-api/fixtures/`. What shape do the mock responses take? What would need to change if the application expected a JSON object instead of a prose response?

Write a brief note on:
- what the application would need to validate
- what failure modes exist if the model produces invalid JSON
- what the retry strategy should look like

## Step 5 - Read a Streaming Response

Open `platform/docker/ai-gateway-service/app.py` and locate the gateway's response path. Does it support streaming? How does it handle chunked responses? Does it log the complete response before returning?

Make a note of what would need to change to add streaming support if it is not already present.

## Step 6 - Compare Model Sources

Review the provider list in `projects/project-01-model-api/config/app.example.json`. How many providers are defined? Are any of them hosted API providers versus mock/local providers?

Consider: if you added a real hosted API provider and a real self-hosted provider, which configuration differences would matter for security (secrets, endpoint URLs) and for reliability (timeouts, fallback)?

## Step 7 - Reflection

Write answers in your workbook (`my-notes/module-02.md`):

1. How does the token count change when you double the length of a system prompt?
2. What would a platform observability dashboard need to show for token usage to be useful?
3. Describe one scenario where you would want schema-constrained structured output rather than JSON mode.
4. What would your tool authorization policy look like if a model could call `delete_service`, `restart_deployment`, and `query_metrics`?
