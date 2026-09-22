# Module 02 References

## Tokenization

- [OpenAI Tokenizer (interactive)](https://platform.openai.com/tokenizer) — paste any text to see exact token counts for OpenAI models
- [tiktoken on GitHub](https://github.com/openai/tiktoken) — OpenAI's tokenization library for client-side counting
- [Hugging Face tokenizer documentation](https://huggingface.co/docs/transformers/main_classes/tokenizer) — for open-weight model tokenizers
- [SentencePiece](https://github.com/google/sentencepiece) — Google's tokenizer used by many open-weight model families

## LLM Inference Mechanics

- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — accessible visual explanation of transformer architecture
- [Attention Is All You Need (2017)](https://arxiv.org/abs/1706.03762) — original transformer paper
- [LLM Inference Performance Engineering Best Practices — NVIDIA](https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/) — practical serving optimization guide
- [vLLM: Efficient Memory Management for LLM Serving with PagedAttention](https://arxiv.org/abs/2309.06180) — key paper on KV cache management

## Generation Parameters

- [OpenAI API Reference — Chat Completions](https://platform.openai.com/docs/api-reference/chat/create) — canonical parameter reference for the OpenAI-compatible API surface
- [Temperature and Sampling in Language Models — Hugging Face](https://huggingface.co/blog/how-to-generate) — accessible explanation of sampling strategies

## Structured Outputs

- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — documentation for schema-constrained generation
- [JSON Schema specification](https://json-schema.org/) — reference for the schema language used in structured output definitions
- [Outlines library](https://github.com/outlines-dev/outlines) — open-source constrained generation library for local models

## Tool Calling

- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — reference for the function calling / tool use API
- [Anthropic Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Anthropic's implementation of tool calling
- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/) — standardized protocol for tool and resource exposure

## Streaming

- [Server-Sent Events (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) — reference for the SSE protocol used by LLM streaming
- [OpenAI Streaming](https://platform.openai.com/docs/api-reference/chat/create#chat-create-stream) — OpenAI streaming API documentation

## Hosted vs Self-Hosted

- [vLLM Project](https://github.com/vllm-project/vllm) — high-performance LLM inference and serving engine
- [Ollama](https://ollama.com/) — local model serving for development and small-scale use
- [Text Generation Inference (TGI)](https://github.com/huggingface/text-generation-inference) — Hugging Face serving framework
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) — benchmark comparisons across open-weight models
- [Artificial Analysis](https://artificialanalysis.ai/) — independent latency and cost benchmarks across model providers
