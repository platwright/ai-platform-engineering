# Module 01 Solution

This solution guide focuses on expected understanding and project behavior, not on one exact wording for your workbook answers.

## Expected Conceptual Outcomes

You should end the module with these durable ideas:

- AI is the umbrella term. ML is a subset. Deep learning is a subset of ML. Foundation models and LLMs are modern generative AI artifacts inside that stack.
- Training and inference are different operational problems. Training is artifact creation. Inference is request serving.
- Parameter count matters, but it is not the only operational driver. Precision, quantization, context length, concurrency, and output length all matter.
- Embeddings are an infrastructure concern because they create ingestion, storage, retrieval, and freshness responsibilities.
- The AI lifecycle needs controls just like application delivery pipelines do.

## Expected Mini-Project Success Run

When you run the success fixture, the script should:

- exit with `0`
- write a JSON report file into `project/runs/`
- show a success status code
- include prompt, completion, and total token counts
- include a short assistant response explaining AI, ML, and deep learning

## Expected Mini-Project Failure Run

When you run the rate-limit fixture, the script should:

- exit non-zero
- write a JSON report file anyway
- include a `429` status code
- include an error object with a message and type

That behavior is important. Observability tooling should not lose evidence just because the request failed.

## Example Interpretation

One strong interpretation is:

- status code and error type are log and alert candidates
- latency is a metric candidate
- token usage is both a cost and performance signal
- model name and finish reason are useful trace attributes
- raw response content can be operationally helpful but may need redaction controls

## If You Used A Real Endpoint

Real results will vary, but you should still expect the same basic categories of telemetry:

- request configuration
- status
- latency
- usage
- response text
- error information

If the endpoint did not return usage data, note that gap in your workbook. Missing telemetry is itself a platform finding.