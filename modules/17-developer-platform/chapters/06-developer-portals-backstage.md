# Chapter 06 - Developer Portals (Backstage)

## What Backstage Is

Backstage is an open-source developer portal framework created by Spotify and donated to the CNCF. It provides three core capabilities:

- **Software Catalog**: a registry of all software, services, APIs, teams, and documentation in the organization
- **Scaffolder**: a template engine for generating new applications and platform resources
- **TechDocs**: a documentation site built from markdown in repositories

For the Acme AI platform, Backstage serves as the central entry point where developers discover platform capabilities, provision services, and find documentation.

## The Software Catalog

The catalog is a searchable registry of what exists in the organization:

```yaml
# platform/backstage/catalog/ai-gateway.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: ai-gateway
  title: AI Gateway
  description: Unified model endpoint with routing, rate limiting, and usage tracking
  annotations:
    backstage.io/techdocs-ref: dir:.
    prometheus.io/alert: ai_gateway_error_rate
  tags:
    - ai-platform
    - gateway
    - production-ready
  links:
    - url: http://ai-gateway.internal:8080
      title: Internal Endpoint
    - url: https://wiki.acme.ai/ai-gateway
      title: Documentation
spec:
  type: service
  lifecycle: production
  owner: group:platform-team
  system: ai-platform
  providesApis:
    - ai-gateway-api-v2
  dependsOn:
    - component:project-01-model-api
```

Catalog entries enable developers to:
- discover what platform services exist
- see who owns each service and how to contact them
- find the documentation, runbook, and API spec for each service
- understand dependencies between services

## API Component

Register the platform's API contract in the catalog:

```yaml
# platform/backstage/catalog/ai-gateway-api.yaml
apiVersion: backstage.io/v1alpha1
kind: API
metadata:
  name: ai-gateway-api-v2
  title: AI Gateway API v2
  description: Chat, embedding, and routing API for the Acme AI platform
spec:
  type: openapi
  lifecycle: production
  owner: group:platform-team
  definition:
    $text: ./openapi.yaml  # OpenAPI spec file
```

Backstage renders the OpenAPI spec as browsable documentation in the portal.

## The Scaffolder Template

A Backstage scaffolder template creates a new application from a golden path:

```yaml
# platform/backstage/templates/new-rag-app/template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: ai-rag-app
  title: New RAG Application
  description: Creates a new AI application with RAG integration
  tags: [ai, rag, recommended]
spec:
  type: service
  parameters:
    - title: Application Details
      required: [appName, teamName, ragServiceName]
      properties:
        appName:
          type: string
          title: Application Name
          pattern: "^[a-z][a-z0-9-]{2,30}$"
        teamName:
          type: string
          title: Team Name
        ragServiceName:
          type: string
          title: RAG Service Name
          description: "Must be an existing registered RAG service"
        modelTier:
          type: string
          title: Model Tier
          enum: [standard, premium]
          default: standard

  steps:
    - id: fetch-template
      name: Fetch Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          appName: ${{ parameters.appName }}
          teamName: ${{ parameters.teamName }}
          ragServiceName: ${{ parameters.ragServiceName }}
          modelTier: ${{ parameters.modelTier }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=acme-ai&repo=${{ parameters.appName }}
        defaultBranch: main
        description: "${{ parameters.appName }} AI application"

    - id: register
      name: Register in Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml

  output:
    links:
      - title: Repository
        url: ${{ steps.publish.output.remoteUrl }}
      - title: View in Catalog
        url: ${{ steps.register.output.entityRef }}
```

## TechDocs

TechDocs generates a documentation site from markdown files in repositories. Add a `mkdocs.yml` to any catalog component and its docs appear in the portal:

```yaml
# mkdocs.yml in the AI gateway repo
site_name: AI Gateway
docs_dir: docs
nav:
  - Overview: index.md
  - API Reference: api-reference.md
  - Quickstart: quickstart.md
  - Runbook: runbook.md
```

Keeping docs in the repository (docs-as-code) means documentation is updated alongside code and reviewed in pull requests, rather than on a separate wiki that drifts out of sync.

## Running Backstage Locally

For the course, run Backstage locally using the `platform/backstage/` assets:

```bash
cd platform/backstage
npm install
npm run dev
```

The portal is available at `http://localhost:3000`. Load the initial catalog entries:

```bash
# Backstage will auto-discover catalog files specified in app-config.yaml
# Or register manually:
curl -X POST http://localhost:7007/api/catalog/locations \
  -H "Content-Type: application/json" \
  -d '{"type": "url", "target": "file:../catalog/ai-gateway.yaml"}'
```
