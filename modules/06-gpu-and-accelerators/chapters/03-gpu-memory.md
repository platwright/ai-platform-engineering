# Chapter 6.3 - GPU Memory

GPU memory is one of the most important serving constraints for LLM workloads.

It is consumed by:

- model weights
- KV cache
- runtime activations and overhead

That is why parameter count, precision, batch size, and context length all show up again during inference discussions.