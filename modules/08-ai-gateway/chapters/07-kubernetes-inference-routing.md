# Chapter 8.7 - Kubernetes Inference Routing

Inference routing on Kubernetes matters because model-serving backends do not behave like ordinary stateless HTTP services. Traffic steering can benefit from awareness of model state, capacity, and serving-specific constraints.