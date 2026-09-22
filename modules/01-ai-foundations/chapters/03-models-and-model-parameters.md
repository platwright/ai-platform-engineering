# Chapter 1.3 - Models and Model Parameters

## Why This Chapter Matters

Platform teams constantly hear shorthand such as "7B model," "128k context," or "4-bit quantized." Those phrases are not research trivia. They are signals about memory, cost, latency, deployment constraints, and operational tradeoffs.

## Parameters And Weights

Parameters are the learned numeric values inside a model. Weights are the practical values stored after training. In casual usage, engineers often treat the terms as closely related.

Higher parameter counts usually suggest a larger and more capable model class, but that does not automatically mean it is the right production choice.

## Model Size

Model size is influenced by:

- parameter count
- precision format
- architecture details
- whether the model is quantized

A 7B model stored in one precision format may have very different runtime characteristics from the same model quantized into a more compact format.

## Precision

Precision describes how numeric values are represented. Common examples include:

- FP32
- FP16
- BF16
- INT8
- INT4

Lower precision can reduce memory usage and improve serving efficiency, but it may affect output quality or compatibility depending on the model and runtime.

## Quantization

Quantization converts model weights to more compact representations. This can make self-hosting much more practical.

For platform engineers, quantization is a classic tradeoff:

- lower memory footprint
- cheaper serving
- potentially lower accuracy or changed behavior
- runtime compatibility considerations

## Context Window

The context window is the amount of input history a model can consider in one request. Larger context windows can help with long documents or long conversations, but they also influence:

- memory pressure
- latency
- cost
- prompt construction complexity

## Tokens

Tokens are the units the model processes, not the same thing as words. Billing, throughput, latency, and context usage often all depend on tokens.

Platform implications:

- long prompts increase pre-processing and cost
- long outputs increase response duration and downstream load
- token counts become core observability fields

## Bigger Is Not Always Better

A larger model may provide better quality for some tasks, but smaller models can still win in production when you care about:

- latency
- cost
- privacy constraints
- deployment footprint
- throughput under concurrency

## What To Remember

When someone says a model is "small" or "large," ask which dimension they mean: parameter count, precision, context window, latency, or cost. Those are related, but not identical.