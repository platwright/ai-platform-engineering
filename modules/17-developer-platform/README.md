# Module 17 - Developer Platform

## Overview

The internal AI platform built across this course is powerful, but it is hard to consume without a developer-facing layer. This module shifts focus from platform internals to platform productization: the interfaces, templates, and experiences that let application teams adopt the platform without becoming infrastructure experts.

A platform without a developer experience strategy is a platform that only its builders can use effectively. This module covers self-service design, golden paths, internal APIs, governance without bottlenecks, developer portals, and platform team organization.

## Learning Objectives

By the end of this module, you should be able to:

- design a self-service platform interface for an AI platform
- define golden path templates for common AI application patterns
- expose platform capabilities through stable, versioned internal APIs
- design an onboarding experience that minimizes time-to-first-value
- apply governance mechanisms that enforce standards without creating approval bottlenecks
- register platform services in a Backstage software catalog
- measure platform adoption and identify where developers get stuck
- describe platform team topologies and when each model applies

## Prerequisites

- Completion of [modules/16-ai-finops/README.md](../16-ai-finops/README.md)
- Completion of all Projects (01 through 04)
- Familiarity with Backstage is helpful but not required

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [Self-Service Platform Design](chapters/01-self-service-platform-design.md)
2. [Golden Paths and Templates](chapters/02-golden-paths-and-templates.md)
3. [Platform APIs and Contracts](chapters/03-platform-apis-and-contracts.md)
4. [Developer Onboarding Experience](chapters/04-developer-onboarding-experience.md)
5. [Governance Without Bottlenecks](chapters/05-governance-without-bottlenecks.md)
6. [Developer Portals (Backstage)](chapters/06-developer-portals-backstage.md)
7. [Platform Metrics and Adoption Tracking](chapters/07-platform-metrics-and-adoption-tracking.md)
8. [Platform Team Topologies](chapters/08-platform-team-topologies.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [platform/backstage/README.md](../../platform/backstage/README.md)
- [projects/final-ai-platform/README.md](../../projects/final-ai-platform/README.md)

## Expected Outcome

At the end of this module, you should have:

- a Backstage catalog YAML file registering the AI gateway as a platform component
- a written golden path template for a new RAG-powered application
- a designed onboarding experience for a new team joining the Acme AI platform
- notes on which platform team topology fits the Acme AI organizational context

## Knowledge Check

1. Why does a powerful platform with no self-service experience fail to achieve adoption?
2. What is the difference between a golden path and a mandate? Why does the distinction matter?
3. Why should a platform API be treated with the same stability discipline as a product API?
4. What is "time-to-first-value" and why is it a platform metric, not just a documentation metric?
5. What is the difference between governance through guardrails and governance through approval queues? Which scales better?
6. What does a Backstage software catalog entry enable that a wiki page does not?
7. What is the "platform tax" and how do you measure whether it is too high?

## Common Mistakes

- building a platform that requires teams to understand how it works internally before they can use it
- treating golden paths as documentation that describes what teams should do, rather than automation that makes it easy
- publishing internal platform APIs without stability guarantees, then changing them frequently
- measuring platform success by the number of features deployed rather than by developer adoption metrics
- creating governance that requires platform team approval for every deployment
- assuming a developer portal alone constitutes a developer experience

## Production Considerations

- golden path templates need maintenance; outdated templates produce platforms that don't work
- internal API versioning must be enforced — a breaking change to a platform API is an incident for every consumer
- onboarding metrics should be reviewed quarterly and compared to a baseline
- platform team bandwidth is a limiting factor — self-service reduces toil but does not eliminate it
- team topology should be revisited as the organization scales; what works at 5 teams fails at 50

## Next Step

Read [concepts.md](concepts.md), then work through the Backstage catalog exercise in [lab.md](lab.md) before moving to [modules/18-capstone/README.md](../18-capstone/README.md).

## Overview

The internal AI platform that Acme AI has built across the course is powerful but hard to consume without a developer-facing layer. This module shifts the focus from platform internals to platform productization: the interfaces, templates, and experiences that let application teams adopt the platform without becoming infrastructure experts.

Platform engineering without a developer experience strategy produces a platform that only the people who built it can use effectively. This module covers self-service design, golden paths, internal APIs, and governance without bottlenecks.

## Intended Learning Objectives

By the end of this module, learners should be able to:

- design a self-service platform interface for an AI platform
- define golden path templates for common AI application patterns
- expose platform capabilities through stable internal APIs
- design an onboarding experience that reduces time-to-first-value for application teams
- apply governance mechanisms that maintain standards without creating bottlenecks
- describe how Backstage or similar developer portals can surface AI platform capabilities

## Prerequisites

- Completion of Module 16 (AI FinOps)
- Familiarity with Backstage or internal developer portal concepts (helpful but not mandatory)
- Completion of all Projects (01 through 04)

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Planned Chapter Structure

1. Self-Service Platform Design
2. Golden Paths and Templates
3. Platform APIs and Contracts
4. Developer Onboarding Experience
5. Governance Without Bottlenecks
6. Developer Portals (Backstage)
7. Platform Metrics and Adoption Tracking
8. Platform Team Topologies

## Planned Module Assets

- concepts.md
- architecture.md: developer platform topology showing the self-service layer over the AI platform
- lab.md: create a Backstage software catalog entry for the AI gateway and at least one platform template
- challenge.md
- verification.md
- solution.md
- references.md

## Planned Lab Scope

The lab will:

1. Set up a local Backstage instance from the `platform/backstage/` assets
2. Register the AI gateway, RAG platform, and agent platform as Backstage catalog components
3. Create a minimal Backstage scaffolder template for a new AI-powered application
4. Walk through the developer onboarding experience using the template

## Key Platform Experience Principles This Module Will Cover

- A golden path lowers the cost of doing the right thing
- Platform APIs should be versioned and documented with the same discipline as product APIs
- Onboarding time is a platform metric — track it
- Self-service does not mean self-management of platform internals
- Governance through templates is lighter than governance through approval queues

## Production Considerations This Module Will Address

- How do you maintain a golden path when the platform evolves underneath it?
- What makes a platform API different from an internal service API?
- How do you measure platform adoption and identify where developers get stuck?
- What is the right team topology for a platform team that serves many application teams?

## Next Step

This module will be written in Phase 6. See [modules/18-capstone/README.md](../18-capstone/README.md) for the final module.