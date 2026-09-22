# Project 04 Concepts

## Tools Need Contracts

An agent platform should know what tools exist, what they do, and which ones are dangerous. That is why this project uses a discoverable local tool registry instead of hiding tool calls in arbitrary code.

## Querying Platform Services Is A Real Use Case

The first useful agents inside a platform organization often query existing services and metrics rather than taking broad external actions.

## Approval Gates Matter

Destructive actions should require approval. This project keeps that visible through an approval token requirement for service deletion.

## Auditability Is Part Of Safety

A useful agent run artifact should capture:

- objective
- planned steps
- tools called
- results returned
- whether approval was required

That makes agent behavior reviewable instead of mysterious.