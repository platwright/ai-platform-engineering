# Module 18 - Capstone

## Overview

The capstone assembles everything built across the course into a single coherent platform story. It is not a new technical topic — it is a final synthesis, review, and presentation exercise designed to produce something that learners can genuinely discuss in an interview, architecture review, or technical interview.

By the end of this module, you will have a documented, observable, secured, and cost-attributed AI platform you can explain end to end.

## Learning Objectives

By the end of this module, you should be able to:

- assemble and validate the full Acme AI platform from end to end
- perform an operational review covering observability, security, reliability, and cost
- defend every major platform design decision in terms of tradeoffs rather than technology preferences
- explain what would need to change to take this platform from local to production scale
- present an architecture narrative that connects infrastructure choices to business outcomes
- answer common AI platform engineering interview questions grounded in what you actually built

## Prerequisites

- Completion of all preceding modules (00 through 17)
- Projects 01 through 04 working in the local environment
- A workbook with notes from each module
- The platform assembled at least once end-to-end

## Difficulty And Time

- Difficulty: Advanced (synthesis, not new concepts)
- Estimated time: 8 to 12 hours

## Capstone Structure

This module is structured differently from all previous modules. There are no chapter files. Instead there are four capstone artifacts:

1. [Assembly Checklist](assembly-checklist.md) — bring the full platform online and validate every layer
2. [Operational Review](operational-review.md) — run a structured review covering all operational dimensions
3. [Architecture Narrative Template](architecture-narrative-template.md) — fill-in-the-blank template for your platform narrative
4. [Interview Guide](interview-guide.md) — practice questions with rubric guidance

Work through them in order.

## The Final AI Platform Project

The capstone connects to [projects/final-ai-platform/README.md](../../projects/final-ai-platform/README.md), which provides the consolidated reference architecture and deployment guide for the completed platform.

## Expected Capstone Artifacts

When you finish the capstone, your workbook should contain:

- `my-solutions/capstone-assembly.md` — completed assembly checklist with your observations
- `my-solutions/capstone-operational-review.md` — completed operational review
- `my-solutions/capstone-architecture-narrative.md` — your platform narrative
- `my-notes/capstone-interview-prep.md` — your practice answers

## What "Complete" Looks Like

The capstone is complete when you can:

- Start the full platform stack from scratch and reach a working state in under 2 hours
- Answer all knowledge check questions from every module without referencing the material
- Explain every design decision made in this course and articulate one alternative you considered
- Describe in concrete terms what the top three production-readiness gaps are in the local implementation

## Knowledge Check

These questions span the full course. Answer them without looking at module material:

1. Draw the full Acme AI platform architecture from the application tier through the developer portal. Label every layer.
2. A user reports that responses became worse last week but there are no HTTP errors. Walk through your diagnosis procedure.
3. Your AI platform spend doubled month-over-month with no change in user volume. What is your investigation plan?
4. A new team wants to build a document Q&A feature using the platform. Walk them through the full path from first contact to production.
5. A security audit identified that one tenant's RAG queries could theoretically return another tenant's documents under specific conditions. Describe the fix.
6. An AI agent incorrectly deleted a production RAG service. How did this happen, what stopped it (or should have stopped it), and what changes do you make?
7. You are joining a new organization as an AI platform engineer. What do you assess in the first 30 days?

## Next Step

Start with [assembly-checklist.md](assembly-checklist.md).