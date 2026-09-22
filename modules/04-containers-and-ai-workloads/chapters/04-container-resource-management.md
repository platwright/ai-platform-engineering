# Chapter 4.4 - Container Resource Management

Container resource management matters because AI workloads can consume memory and CPU in uneven ways.

The first signals to reason about are:

- memory footprint
- concurrent request behavior
- startup behavior
- caching behavior

OOM events are especially useful to study because they turn vague capacity assumptions into visible failure.