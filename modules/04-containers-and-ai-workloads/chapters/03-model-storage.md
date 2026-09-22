# Chapter 4.3 - Model Storage

Model assets do not have to live inside container images.

Common options include:

- baking small assets into the image
- downloading from object storage at startup
- mounting from a persistent volume
- using a model registry or cache

Each option changes startup time, network dependence, immutability, and operational control.