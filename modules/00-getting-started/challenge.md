# Module 00 Challenge

## Challenge Prompt

You are the first platform engineer at Acme AI. Two application teams want to ship AI features quickly, but they do not want to own model routing, prompt versioning, observability, or infrastructure operations.

Write a one-page proposal in your workbook that answers:

1. What should application teams own?
2. What should the AI platform team own?
3. What capabilities should the first version of the platform provide?
4. Which parts can stay local or lightweight at first?
5. Which risks would you prioritize before allowing production usage?

## Constraints

- Do not assume a GPU cluster is available on day one.
- Do not assume every team uses the same model provider.
- Do not assume the company is ready for a full internal developer portal yet.

## Deliverable

Store your answer in:

- `my-solutions/module-00-platform-proposal.md`

## What Good Looks Like

A strong answer should:

- separate platform responsibilities from application responsibilities clearly
- prefer a minimal but extensible first platform
- identify observability, secrets, and access control early
- show why local-first learning still maps to production concerns later