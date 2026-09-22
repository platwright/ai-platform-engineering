# Module 06 Solution

## Expected Outcome

A correct completion shows that you can reason about accelerator-backed workloads with more than hand-wavy phrases such as "it needs a GPU."

## What The Estimator Should Teach

The main lesson is relative behavior:

- lower precision reduces weight memory
- larger context and batch sizes increase KV cache pressure
- headroom matters because the theoretical minimum is not the same as a safe operating target

## What The Kubernetes Examples Should Teach

GPU requests change placement assumptions immediately. The examples are useful even without a live GPU cluster because they make scheduling intent explicit.