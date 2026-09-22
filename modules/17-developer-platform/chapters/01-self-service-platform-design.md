# Chapter 01 - Self-Service Platform Design

## What Self-Service Means

Self-service means a developer can access platform capabilities without filing a ticket, waiting in a queue, or asking a platform team member for help. It does not mean the developer manages the underlying infrastructure. The platform team still owns and operates everything underneath; they have just packaged it in a way that is consumable.

Self-service is the difference between:

```
Developer: "I need a RAG service for my team"
                    ↓
         Platform team ticket queue (days to weeks)
                    ↓
         Platform engineer provisions the service
                    ↓
         Developer finally starts building

vs:

Developer: "I need a RAG service for my team"
                    ↓
         Developer portal → "Create RAG Service" form
                    ↓
         Service provisioned in 2 minutes
                    ↓
         Developer immediately starts building
```

## Why Most Platforms Fail At Self-Service

The capability exists but the interface does not. A platform team might have built a powerful RAG-as-a-service capability (Project 03), but if accessing it requires:

- knowing the CLI flags
- reading a 40-page wiki page
- having the right Kubernetes access
- understanding the state directory structure

...then it is not self-service. It is expert service that happens to have a technical interface.

## Designing For Developer Goals, Not Platform Features

Platform documentation organized around features ("Our platform has: gateway, RAG, agents, GPU serving") fails the developer whose first question is: "I want to build a document Q&A feature. How do I start?"

Design self-service around developer jobs-to-be-done:

| Developer Goal | Platform Entry Point |
|---|---|
| Build a new AI chat application | Golden path template: `ai-chat-app` |
| Add RAG to an existing app | Step-by-step guide: "Connecting RAG to your app" |
| Run my prompts against a cheaper model | Gateway routing guide |
| Check why my app's responses got slower | Observability dashboard link |
| See how much my team's AI usage costs | FinOps showback report |

Each entry point takes the developer directly to what they need, framed in terms of their goal — not the platform's architecture.

## The Self-Service Maturity Ladder

Platforms evolve from low to high self-service maturity:

| Level | Description | How To Recognize It |
|---|---|---|
| 1 - Manual | Every request goes through the platform team | Tickets, Slack messages to platform engineers |
| 2 - Documented | Teams can do things themselves if they read the docs | Developers still get stuck and ask for help |
| 3 - Guided | Step-by-step guides with verification | Developers follow guides but hit edge cases |
| 4 - Templated | Scaffolded starting points that work out of the box | New apps start from templates and just work |
| 5 - Self-healing | Platform detects and resolves common problems automatically | Developers rarely contact the platform team |

Most organizations at Level 2 believe they are at Level 4 because they have documentation. The test: time how long it takes a developer unfamiliar with the platform to complete a typical task. That time is the real measure.

## Platform Product Thinking

Platform teams should apply product management practices to their platform:

- **User research**: talk to developers, observe where they get stuck
- **Job stories**: "When I want to [goal], I need [capability] so I can [outcome]"
- **Funnel analysis**: where in the onboarding journey do developers drop off?
- **NPS/satisfaction**: do developers recommend the platform to colleagues?
- **Roadmap transparency**: what is coming, what is not coming, and why

A platform team that ships features without measuring adoption is optimizing for the wrong thing.
