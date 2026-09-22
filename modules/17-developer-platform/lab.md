# Module 17 Lab

## Goal

Register the AI gateway and RAG platform as Backstage catalog components, design a golden path template for a new RAG application, and write an onboarding experience outline.

## Prerequisites

- Backstage CLI available: `npx @backstage/create-app` or a local Backstage installation
- Python 3.11+ and Project 01-04 background knowledge

No live Backstage instance is required for most lab steps. The catalog YAML and template files are valid standalone artifacts.

## Step 1 - Write The AI Gateway Catalog Entry

Create `platform/backstage/catalog/ai-gateway.yaml`:

```yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ai-gateway
  title: AI Gateway
  description: Unified model endpoint with routing, rate limiting, and usage tracking
  tags: [ai-platform, gateway, production-ready]
  links:
    - url: http://localhost:8080
      title: Local Development Endpoint
spec:
  type: service
  lifecycle: production
  owner: group:platform-team
  system: ai-platform
  providesApis:
    - ai-gateway-api
```

Create the accompanying API entry at `platform/backstage/catalog/ai-gateway-api.yaml`:

```yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: ai-gateway-api
  title: AI Gateway API
  description: Chat and routing API — POST /api/chat returns a model response
spec:
  type: openapi
  lifecycle: production
  owner: group:platform-team
  definition: |
    openapi: "3.0.0"
    info:
      title: AI Gateway
      version: "2.0"
    paths:
      /api/chat:
        post:
          summary: Send a chat message
          requestBody:
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message: {type: string}
                    provider: {type: string}
          responses:
            "200":
              description: Model response with usage metadata
```

## Step 2 - Write The RAG Platform Catalog Entry

Create `platform/backstage/catalog/rag-platform.yaml` following the same pattern. Include:

- Component name: `rag-platform`
- Description that explains what RAG-as-a-service means
- A `providesApis` reference
- At least two meaningful tags

## Step 3 - Write A Golden Path Template Definition

Create `platform/backstage/templates/new-rag-app/template.yaml` using the scaffolder template YAML format from Chapter 06. The template should:

- Accept `appName`, `teamName`, `ragServiceName`, and `modelTier` as parameters
- Include validation (required fields, pattern for appName)
- Define at least three scaffolder steps
- Produce an `output.links` section

You do not need a live Backstage instance to validate the YAML — review it against the Backstage scaffolder schema.

## Step 4 - Design The Onboarding Flow

Write a developer onboarding flow for the Acme AI platform in `my-notes/module-17-onboarding.md`.

The flow should have exactly 6 steps, each with:
- A title
- The developer action required
- The expected outcome (what they see if it worked)
- The error condition (what the error message says if it fails)

Target TTFV: a developer should be able to complete all 6 steps in under 60 minutes.

## Step 5 - Design The Governance Policy

Write a one-page governance policy for the Acme AI platform in `my-notes/module-17-governance.md`.

Cover:
1. What requires no review (using a golden path template with default settings)
2. What requires async review within 48 hours (deviating from template defaults)
3. What requires synchronous review (new capabilities not covered by any template)
4. How the exception process works (one paragraph)

## Step 6 - Reflection

In `my-notes/module-17.md`:

1. What is the biggest barrier to self-service adoption at an organization you know?
2. Describe a situation where a governance requirement became a bottleneck. How would you redesign it as a guardrail instead?
3. Which Team Topologies interaction mode is most common between the platform team and application teams in this course? Should it evolve?
4. If you were a new developer joining Acme AI, what would be the first thing you would look for in the developer portal?
