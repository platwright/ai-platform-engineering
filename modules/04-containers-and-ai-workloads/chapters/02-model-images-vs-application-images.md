# Chapter 4.2 - Model Images vs Application Images

Application images and model-serving images solve different problems.

Application images usually package business logic, prompts, and API surfaces. Model-serving or model-access images package inference transport and model-facing concerns. Combining them too early can make images unnecessarily large, slow to rebuild, and harder to secure.

This is why the repository keeps the sample chat app and Project 01 in separate images.