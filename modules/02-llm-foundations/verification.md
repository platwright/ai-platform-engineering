# Module 02 Verification

## Check 1 - Tokenization Understanding

Answer the following without looking at the chapter:

1. Approximately how many tokens is a 1,000-word English document?
2. Why does a larger context window not necessarily mean better performance?
3. What happens to serving concurrency when many requests use near-maximum context length?

If you cannot answer these, reread [chapters/01-tokenization-and-context-windows.md](chapters/01-tokenization-and-context-windows.md).

## Check 2 - Token Usage in Run Artifacts

Open a recent run artifact from `projects/project-01-model-api/runs/`. Confirm:

- [ ] `prompt_tokens` is present and non-zero
- [ ] `completion_tokens` is present and non-zero
- [ ] `total_tokens` equals the sum of the above two fields
- [ ] You can explain why `prompt_tokens` is the number it is

## Check 3 - Generation Parameter Awareness

Review the provider configuration or application code and confirm:

- [ ] `max_tokens` is set to an explicit value, not unbounded
- [ ] `temperature` is set explicitly or you can identify the default being used
- [ ] You can explain what would happen if `max_tokens` was removed

## Check 4 - Structured Output Understanding

Confirm you can describe the difference between:

- [ ] JSON mode response format
- [ ] Schema-constrained structured output
- [ ] Post-generation validation

Write one sentence for each describing what it guarantees.

## Check 5 - Tool Calling Protocol

Without looking at the chapter, sketch the tool calling loop:

1. What does the application send to the model?
2. What does the model send back when it wants to call a tool?
3. What does the application do next?
4. What does the application send to the model to continue?
5. What does the model send back as its final response?

## Check 6 - Streaming Awareness

Confirm you can answer:

- [ ] What is TTFT and why does it differ from end-to-end latency?
- [ ] Name two infrastructure components that could silently break streaming without returning an error
- [ ] What does the platform need to do to log complete responses when streaming is enabled?

## Check 7 - Hosted vs Self-Hosted

For each statement, decide whether it describes hosted APIs, self-hosted models, or both:

- [ ] Per-token billing applies
- [ ] You own GPU provisioning and incident response
- [ ] Rate limits can affect production traffic without warning
- [ ] Data never leaves your network boundary
- [ ] Access to frontier model capabilities is available today
- [ ] Fine-tuning and quantization are possible
