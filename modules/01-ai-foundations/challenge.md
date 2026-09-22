# Module 01 Challenge

## Challenge Prompt

You are the first engineer responsible for defining the AI workload taxonomy at Acme AI. Product teams are asking for:

- a chat assistant
- nightly document indexing
- semantic search over internal docs
- a support summarization batch job
- an agent that can call internal tools

Classify each workload and propose the operational treatment it should receive.

## Deliverables

Create a short design note in:

- `my-solutions/module-01-workload-taxonomy.md`

Your note should include:

1. workload type
2. synchronous or asynchronous behavior
3. latency sensitivity
4. likely compute profile
5. failure handling expectation
6. what you would observe first

## Mini-Project Extension

Run the observer three ways if you can:

1. mock success
2. mock rate limit failure
3. real endpoint success or an intentionally invalid endpoint configuration

Then answer:

- which errors should trigger retries
- which errors should fail fast
- which metadata would you need for cost controls later

## What Good Looks Like

A strong answer should separate user-facing inference from background jobs, connect retrieval and embeddings to platform services, and show that agent workloads introduce different risk and observability needs than plain text generation.