# Chapter 06 - Hosted vs Self-Hosted Models

## The Core Decision

Every AI platform must decide where models run:

- **Hosted**: call a third-party API (OpenAI, Anthropic, Gemini, Cohere, Mistral API, etc.)
- **Self-hosted**: download a model artifact and run it on your own compute

This is not a one-time architectural choice. Most production platforms end up with a mix of both, and the allocation shifts as cost, capability, and privacy requirements evolve.

## Hosted Model APIs

### How They Work

Hosted APIs expose model inference over HTTPS using a standardized request/response format. The OpenAI chat completions API (`/v1/chat/completions`) has become a de facto standard that many providers implement.

You send a request. The provider runs it on their infrastructure. You get a response and an invoice.

### Advantages

**Zero infrastructure burden**: no GPUs, no model weights, no serving software, no cluster management.

**Access to frontier capabilities**: state-of-the-art models like GPT-4o, Claude Opus, and Gemini Ultra are only available via hosted APIs.

**Instant scaling**: the provider absorbs traffic bursts. You do not provision capacity.

**Operational simplicity**: authentication, versioning, and updates are the provider's responsibility.

### Risks and Limitations

**Data privacy**: prompts and responses transit a third-party system. For regulated industries or sensitive data, this is a compliance risk that may require a data processing agreement (DPA) or may simply be unacceptable.

**Cost at scale**: per-token billing compounds quickly. A system handling 10M tokens per day at $5/1M tokens costs $50/day, or roughly $18,000/year, for that one model. High-throughput applications often find self-hosting cheaper beyond a break-even point.

**Provider dependency**: rate limits, outages, API changes, model deprecations, and pricing adjustments are outside your control.

**Latency from geography**: requests travel to the provider's data centers. Network round-trip adds to TTFT, especially for users far from the provider's regions.

**Quota constraints**: hosted APIs often have request-per-minute and token-per-minute quotas. Burst traffic can hit limits even with paid access.

## Self-Hosted Open-Weight Models

### What Open-Weight Means

Open-weight models release the trained model weights publicly. Prominent examples:

| Model family | Organization | Notes |
|---|---|---|
| Llama 3 | Meta | Wide community adoption |
| Mistral / Mixtral | Mistral AI | Strong performance per parameter |
| Qwen | Alibaba | Strong multilingual and code performance |
| Gemma | Google DeepMind | Lightweight, runs on consumer hardware |
| Phi | Microsoft | Small but capable for specific tasks |
| DeepSeek | DeepSeek AI | Strong reasoning and code |

Note: open-weight is not the same as open-source. Some open-weight licenses restrict commercial use or require attribution. Always review the model license before production deployment.

### Serving Infrastructure

Self-hosted models need:

- **Model weights**: typically 4–70GB depending on model size and quantization
- **GPU compute**: most serious serving uses NVIDIA A10G, A100, or H100 GPUs
- **Serving software**: vLLM, TGI, Ollama, llama.cpp, or similar
- **Container and orchestration layer**: Docker or Kubernetes

Lower-end options (Ollama on consumer hardware) work for development and small-scale use. Production serving typically requires dedicated GPU nodes.

### Advantages

**Data privacy and sovereignty**: data never leaves your infrastructure.

**No per-token billing**: beyond infrastructure cost, each token is free.

**Customization**: fine-tune, quantize, or modify behavior in ways hosted APIs do not permit.

**No rate limits**: you control the capacity.

**Predictable cost**: infrastructure cost is fixed or scales predictably with hardware additions.

### Costs and Risks

**Operational burden**: you own GPU provisioning, model loading, serving stability, scaling, updates, and incident response.

**Capability gap**: open-weight frontier models trail proprietary frontier models in some benchmarks. This gap is closing but matters for complex reasoning tasks.

**Quantization tradeoffs**: running quantized models (INT4, INT8) reduces memory and cost but degrades output quality in measurable ways depending on the task.

**Hardware availability**: GPU availability is constrained. Planning and procurement cycles are longer than calling an API.

## The Hybrid Strategy

Most mature AI platforms route intelligently across both hosted and self-hosted:

```
Simple Q&A, classification    → fast self-hosted small model (e.g., Llama 3 8B)
Complex reasoning, drafts     → frontier hosted model (e.g., GPT-4o, Claude Sonnet)
Sensitive internal data       → self-hosted private model
Batch processing jobs         → self-hosted for cost efficiency
User-facing interactive chat  → hosted for reliability and TTFT guarantees
```

An AI gateway handles routing decisions, making the choice transparent to applications.

## Cost Comparison Framework

Estimating break-even between hosted and self-hosted:

```
Hosted cost = (tokens_per_month / 1_000_000) × provider_rate_per_M_tokens
Self-hosted cost = (gpu_hours_per_month × gpu_rate) + cluster_overhead

Break-even: when self-hosted_cost < hosted_cost
```

Practical considerations that shift the calculation:

- GPU instances are often reserved for 1–3 years (up to 60% discount vs on-demand)
- Utilization matters: a GPU at 20% utilization has effectively 5x higher per-token cost than a GPU at 100%
- Serving multiple models on the same GPU (multiplexing) improves economics
- Engineering time to operate GPU infrastructure has real cost

A common rough threshold: if you are spending more than $5,000–$10,000/month on hosted inference for a single model, a self-hosted alternative is likely worth evaluating.

## Model Selection Criteria

When choosing any model (hosted or self-hosted), evaluate:

| Criterion | Questions to ask |
|---|---|
| Capability | Does this model perform well on the actual tasks we need? |
| Context window | Is the window sufficient for our retrieval and conversation patterns? |
| Language support | Does the model handle the languages our users write in? |
| License | Are commercial use, redistribution, and fine-tuning permitted? |
| Latency | Does TTFT and generation speed meet our UX requirements? |
| Cost | What is the total cost at our current and projected volume? |
| Stability | How often does the provider update or deprecate the model? |
| Privacy | Does data handling meet our regulatory requirements? |

## Platform Design Implications

The hosted/self-hosted decision shapes the platform in several ways:

- **Model routing** in the AI gateway must express routing logic in terms of capability, cost, and privacy
- **Evaluation pipelines** must validate behavior across whichever models are in use
- **Operational runbooks** for self-hosted models need GPU health, OOM, and model-load incident procedures
- **Cost attribution** for self-hosted vs hosted models uses different accounting models (GPU hours vs token counts)
- **Fallback chains** often cross the hosted/self-hosted boundary as a reliability strategy

## Summary

| | Hosted APIs | Self-Hosted |
|---|---|---|
| Setup time | Minutes | Days to weeks |
| Operational burden | Low | High |
| Data privacy | Third-party | Controlled |
| Cost model | Per-token | Infrastructure |
| Scale at volume | Elastic | Fixed capacity |
| Customization | Limited | Full |
| Access to frontier | Yes | Lagging |
| Rate limits | Provider-imposed | None |
