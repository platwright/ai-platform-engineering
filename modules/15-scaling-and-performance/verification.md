# Module 15 Verification

## Check 1 - Latency Decomposition

List the stages in a RAG request latency waterfall in order. For each, state one factor that would make it longer.

## Check 2 - Benchmark Output

After running the mock benchmark, confirm:
- [ ] You can identify the TTFT figure in the output
- [ ] You can identify the tokens-per-second figure
- [ ] You can explain what "concurrency" means in the context of this benchmark

## Check 3 - Autoscaling Design

Without looking at the chapter, explain:

1. Why is CPU utilization a poor autoscaling metric for model serving pods?
2. What metric should you use instead?
3. Why is there a cooldown period before scaling down?

## Check 4 - Scaling Decision

For each scenario, state whether scale-up or scale-out is the correct response and why:

1. A 7B model fits on an A10G, but throughput is insufficient for the request volume
2. A 70B model requires more memory than one A100 80GB provides
3. TTFT is within SLO but total cost per inference is too high
4. Users in a remote region experience high network latency to the serving endpoint

## Check 5 - Continuous Batching

Explain in plain language:
- How does continuous batching differ from dynamic batching?
- Why does it improve both throughput and TTFT compared to static batching?
- What vLLM configuration enables continuous batching?

## Check 6 - Latency Measurements

Your latency decomposition from the lab:
- [ ] All four stages are timed (embed, search, rerank, LLM)
- [ ] LLM generation dominates total latency (expected)
- [ ] You can explain what would make each stage slower
- [ ] You ran at least 5 queries and have a p50 and p95 estimate

## Check 7 - Load Test Understanding

Describe what your load test from the lab (or the designed scenario) would tell you that a simple `curl` loop would not.

## Check 8 - Quantization Awareness

You should be able to explain:
- [ ] What INT8 quantization means and its typical memory reduction
- [ ] Why you should always run your evaluation suite after quantizing a model
- [ ] One scenario where INT4 quantization would be acceptable
- [ ] One scenario where it would not be acceptable
