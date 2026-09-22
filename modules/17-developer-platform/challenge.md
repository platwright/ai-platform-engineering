# Module 17 Challenge

## Challenge 1 - Complete Platform Catalog

Create Backstage catalog YAML for all four major platform services:

1. `ai-gateway` (from the lab)
2. `rag-platform`
3. `agent-platform`
4. `model-serving` (vLLM deployment)

For each component:
- Write a clear description from a developer's perspective
- List the API it provides
- List any services it depends on
- Include at least 3 meaningful tags
- Include links to local endpoints and documentation

Create a `catalog-info.yaml` root file that imports all four components.

## Challenge 2 - Template Skeleton

Create the actual file skeleton for the `ai-rag-app` golden path template under `platform/backstage/templates/new-rag-app/skeleton/`.

The skeleton should produce these files when instantiated:

```
skeleton/
├── README.md              ← uses ${{ values.appName }} and ${{ values.teamName }}
├── app.py                 ← working HTTP application that queries the RAG platform
├── config/
│   └── app.example.json   ← configuration pointing to platform services
├── prompts/
│   └── rag-grounding.yaml ← starter prompt template with versioning metadata
├── eval/
│   └── smoke-cases.json   ← 5 starter eval cases (generic enough to customize)
└── catalog-info.yaml      ← Backstage catalog entry for the new app
```

Each file in the skeleton should have meaningful content — not empty placeholders. The `app.py` should actually call the RAG platform using the same pattern as the existing applications in this course.

## Challenge 3 - API Contract Document

Write a complete API contract document for the AI Gateway `/api/chat` endpoint.

The document should cover:
- All request fields (required and optional) with types and descriptions
- All response fields with types, descriptions, and stability annotations
- All error codes with descriptions and whether they are retriable
- The SLA (availability, latency SLO, error budget)
- The deprecation policy for this endpoint
- A changelog with two entries (one addition, one breaking change from a hypothetical previous version)

Save as `platform/backstage/catalog/ai-gateway-contract.md`.

## Challenge 4 - Onboarding Instrumentation Design

Design an instrumentation plan for the onboarding flow you defined in the lab.

For each of the 6 onboarding steps, define:
- The event name to log when the step is completed
- The event name to log when the step fails
- The metric that would surface drop-off at this step in a dashboard
- The alert condition that would indicate the step is broken for all new developers

Present as a table in `my-solutions/module-17-instrumentation.md`.

## Challenge 5 - Platform Team Charter

Write a one-page platform team charter for the Acme AI platform team.

Include:
- The team's mission in one sentence
- What the team owns and what it does not own
- How teams can request help (and what response time to expect)
- What the team considers a success metric
- How the team handles breaking changes to platform APIs
- What governance authority the team has and where it ends

The charter should be honest about tradeoffs — for example, the team cannot support every customization request.
