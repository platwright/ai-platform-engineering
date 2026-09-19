# Module 00 - Getting Started

## Overview

This module establishes the operating context for the rest of the course. It defines what AI platform engineering is, introduces the platform we will build, verifies the local development environment, and sets up a personal repository workflow.

If the rest of the course is about operating AI systems in production, this module is about making sure you understand the problem space and have a reliable workstation to learn from.

## Learning Objectives

By the end of this module, you should be able to:

- explain what AI platform engineering is and how it differs from adjacent roles
- describe the application, platform, and infrastructure layers of an AI system
- summarize the staged architecture used across the course
- validate a local environment for the early labs
- set up a personal workbook workflow inside your fork

## Prerequisites

- Basic familiarity with Git and the command line
- A machine capable of running Docker and Python tooling
- Review of [docs/prerequisites.md](../../docs/prerequisites.md)

## Difficulty And Time

- Difficulty: Beginner
- Estimated time: 2 to 4 hours

## Module Map

### Chapters

1. [What Is AI Platform Engineering?](chapters/01-what-is-ai-platform-engineering.md)
2. [What We Will Build](chapters/02-what-we-will-build.md)
3. [Local Development Environment](chapters/03-local-development-environment.md)
4. [Repository Workflow](chapters/04-repository-workflow.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Expected Outcome

At the end of Module 00, you should have:

- a working local toolchain for the course baseline
- a fork or local clone organized as your workbook
- a clear mental model of the platform narrative used in the course
- a personal note on how your current role overlaps with AI platform engineering

## Knowledge Check

Use these questions before moving on:

1. Why is AI platform engineering not the same as model training or data science?
2. What sits in the AI application layer versus the platform layer?
3. Why does this course start local-first instead of cloud-first?
4. What practical difference exists between a hosted model integration and self-hosted model serving?
5. Which required tools are optional to install later, and why?

## Common Mistakes

- Treating this course as a prompt engineering course instead of a platform engineering course.
- Skipping environment verification and assuming tools are installed correctly.
- Jumping straight into Kubernetes or GPUs without understanding workload behavior.
- Using the upstream repository as your notebook instead of working from a fork or personal clone.

## Production Considerations

Even in this introductory module, the course framing matters:

- local tools should mirror production concepts without pretending local equals production
- setup automation should be repeatable and visible
- developer workflow should encourage traceability and documentation
- environment drift should be detected early with simple checks

## Next Step

Start with [concepts.md](concepts.md), then read the chapters in order before doing [lab.md](lab.md).