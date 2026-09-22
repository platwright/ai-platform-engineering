# Module 15 Lab

## Goal

Run the Project 02 benchmark at multiple concurrency levels, analyze the results to find the performance boundary, and design an autoscaling policy based on the findings.

## Prerequisites

- Project 02 benchmark tool working (mock mode available without GPU)
- Python 3.11+
- Optional: a local vLLM instance or Ollama endpoint for real measurements

## Step 1 - Run The Mock Benchmark

Run the Project 02 benchmark in mock mode to understand the tool output format:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py --mode mock
```

Examine the output report. Identify:
- What latency metrics are reported?
- Is TTFT measured separately from total latency?
- What concurrency level was used?
- What is the tokens-per-second figure?

## Step 2 - Run At Multiple Concurrency Levels (Mock Mode)

Repeat the benchmark at several concurrency levels and record results:

```bash
# If the benchmark supports a concurrency argument, try:
python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode mock --concurrent 1

python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode mock --concurrent 5

python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode mock --concurrent 10
```

If the benchmark does not have a direct concurrency argument, review the source code to understand how it sends requests and how you could parallelize them.

## Step 3 - Latency Decomposition Exercise

Manually decompose the latency for a single RAG query by timing each stage. Run these in sequence and record the time for each:

```bash
time python -c "
import sys, time
sys.path.insert(0, '.')
from applications.sample_rag import embed_query
start = time.time()
embed_query('What is retrieval freshness?')
print(f'Embed: {(time.time()-start)*1000:.1f}ms')
" 2>/dev/null
```

Or simply run:
```bash
python applications/sample-rag/app.py query \
  --tenant team-a \
  --question "What is retrieval freshness?" \
  --verbose  # if verbose flag exists
```

Record your measured latency breakdown in `my-notes/module-15-latency.md`:
```
Embed query:     ___ms
Vector search:   ___ms
(reranker):      ___ms
LLM generation:  ___ms
Total:           ___ms
```

## Step 4 - Identify The Bottleneck

Based on your latency decomposition, identify:
- Which stage takes the most time?
- Which stage has the highest variance (run 5 queries and compare)?
- If you doubled the number of concurrent users, which stage would degrade first?

## Step 5 - Design An Autoscaling Policy

Write an autoscaling policy for the model serving deployment in `my-notes/module-15-autoscaling.md`.

Include:
1. The primary scaling metric and why CPU is wrong for this workload
2. The target metric value for scaling up (e.g., "scale up when queue depth > N")
3. The minimum and maximum replica counts
4. The cooldown period (why is a cooldown needed?)
5. The scale-down delay and why it should be longer than scale-up

## Step 6 - Optional: Real Benchmark

If you have Ollama running with a model loaded:

```bash
python projects/project-02-ai-gateway/benchmark_openai_compatible.py \
  --mode http \
  --endpoint http://localhost:11434/v1/chat/completions \
  --model llama3.2:3b \
  --requests 20
```

Compare the results to the mock mode numbers. What does this tell you about the mock mode's accuracy as a proxy for real performance testing?

## Step 7 - Reflection

In `my-notes/module-15.md`:

1. Describe the latency waterfall for a RAG request in your own words. Which component are you most likely to need to optimize at production scale?
2. Why would you NOT use standard HPA (CPU-based) to autoscale the model server?
3. Design a 3-line capacity planning statement for the Acme AI platform based on what you now know:
   - "At X concurrent users, the platform serves responses with TTFT ≤ Y seconds"
   - "Beyond Z concurrent users, TTFT exceeds the SLO"
   - "To support 2× more concurrent users, we need..."
