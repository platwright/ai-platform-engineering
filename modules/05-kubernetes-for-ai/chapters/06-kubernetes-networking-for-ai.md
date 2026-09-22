# Chapter 5.6 - Kubernetes Networking for AI

AI networking concerns include more than service discovery. You also care about:

- timeout behavior
- user-facing latency
- ingress routing
- internal model API traffic
- long-lived responses later when streaming is introduced

The sample stack uses Services and an Ingress to make those paths explicit.