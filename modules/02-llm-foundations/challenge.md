# Module 02 Challenge

These challenges extend the core lab without step-by-step guidance. Use the chapter material, run artifacts, and your own research.

## Challenge 1 - Token Budget Calculator

Write a small Python utility that:

1. Reads the system prompt from `projects/project-01-model-api/config/app.example.json`
2. Accepts a user message as input
3. Estimates total token usage before sending the request
4. Warns if the estimated token count exceeds a configurable budget threshold

You do not need a live model for this. Use character count divided by 4 as a rough approximation, or install `tiktoken` for more accurate counting.

Expected output:
```
System prompt: ~320 tokens
User message: ~18 tokens
Estimated total input: ~338 tokens
Budget threshold: 2000 tokens
Status: OK (16.9% of budget used)
```

## Challenge 2 - Generation Parameter Experiments

Run the mock provider with several different temperature and max_tokens combinations. Observe the run artifacts.

Answer:
- What changes between temperature=0.2 and temperature=1.5 output?
- What happens when max_tokens is very small (10-20 tokens)?
- What does a truncated response look like in the run artifact?

Document your findings as a brief parameter guide for your workbook.

## Challenge 3 - Structured Output Validation

Write a small Python function that:

1. Accepts a raw model response string
2. Parses it as JSON
3. Validates it against a minimal schema of your choosing
4. Returns either the validated object or a structured error

Test it with:
- a valid response
- a response that is valid JSON but fails schema validation
- a response that is not valid JSON at all

## Challenge 4 - Tool Schema Design

Design tool schemas for three platform tools:

1. `query_rag` — retrieves information from a named knowledge base
2. `get_service_health` — returns health status for a named platform service
3. `scale_deployment` — adjusts replica count for a Kubernetes deployment

For each tool, write:
- the tool name and description
- the parameter schema
- which parameter combinations should require approval before execution
- what the error response should look like

## Challenge 5 - Model Routing Decision Table

For each of the following scenarios, decide: hosted frontier, self-hosted large, or self-hosted small? Justify each choice in two to three sentences.

1. A customer support chatbot processing 2M tokens/day with no PII in the prompts
2. An internal HR assistant that processes employee records and salary data
3. An automated code review tool that needs strong reasoning for complex architecture questions
4. A document classifier that labels support tickets into one of 12 categories
5. A batch summarization job that processes 50,000 documents per week overnight
