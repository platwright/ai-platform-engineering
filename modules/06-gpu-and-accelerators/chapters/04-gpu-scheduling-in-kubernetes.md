# Chapter 6.4 - GPU Scheduling in Kubernetes

GPU scheduling is more constrained than general compute scheduling because accelerators are scarce, specialized, and expensive.

Kubernetes GPU scheduling typically involves device plugins, resource requests, labels, taints, tolerations, and increasingly richer allocation mechanisms.