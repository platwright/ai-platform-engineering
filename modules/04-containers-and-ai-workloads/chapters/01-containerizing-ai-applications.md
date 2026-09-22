# Chapter 4.1 - Containerizing AI Applications

Containerizing an AI application means packaging its runtime dependencies, code, prompts, and entry point into a repeatable image.

The key idea is repeatability. A container should make the workload more portable and explicit, not more mysterious.

For this course, the sample chat app and Project 01 are containerized separately so that the boundary between application logic and model access remains visible.