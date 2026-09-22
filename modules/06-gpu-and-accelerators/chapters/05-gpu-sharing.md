# Chapter 6.5 - GPU Sharing

GPU sharing exists because idle accelerator time is expensive to waste.

Common strategies include:

- time slicing
- MIG
- fractional GPU access depending on the platform stack

Each strategy improves utilization but changes fairness, isolation, and observability.