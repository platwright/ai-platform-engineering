# Chapter 5.7 - Storage for AI Workloads

Stateless application pods and stateful AI backing services should not be treated the same way.

The sample chat application itself stays mostly stateless, but the Qdrant example introduces persistent storage through a StatefulSet and PVC-backed storage. That distinction becomes more important as retrieval and model-serving workloads grow.