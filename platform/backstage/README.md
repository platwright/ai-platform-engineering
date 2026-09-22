# Backstage And Developer Portal Assets

This area holds self-service platform artifacts, internal developer portal templates, and Backstage catalog definitions for the Acme AI developer experience layer.

## Available Assets

### Catalog Entries (`catalog/`)

| File | Kind | Description |
|---|---|---|
| `ai-gateway.yaml` | Component | AI gateway service with routing and rate limiting |
| `ai-gateway-api.yaml` | API | OpenAPI definition for the `/api/chat` and `/metrics` endpoints |
| `rag-platform.yaml` | Component | RAG-as-a-service platform with per-tenant isolation |
| `agent-platform.yaml` | Component | Safe agent runtime with tool registry and approval gates |

### Golden Path Templates (`templates/`)

| Directory | Purpose |
|---|---|
| `new-rag-app/` | Scaffolder template for a new RAG-powered application |

## Relationship To Module 17

Module 17 (Developer Platform) lab uses these assets to demonstrate self-service platform experiences. The catalog entries formalize what "publishing a platform capability" means from the developer portal perspective. The scaffolder template demonstrates a golden path for application teams.

## Local Setup

To run Backstage locally with this catalog:

```bash
# Initialize Backstage app (only needed once)
npx @backstage/create-app@latest --path platform/backstage/app

# Start the development server
cd platform/backstage/app
yarn dev
```

Then register the catalog entries through the Backstage UI at `http://localhost:3000/catalog-import`, or add this to `app-config.yaml`:

```yaml
catalog:
  locations:
    - type: file
      target: ../../catalog/ai-gateway.yaml
    - type: file
      target: ../../catalog/rag-platform.yaml
    - type: file
      target: ../../catalog/agent-platform.yaml
```

See the Module 17 lab for step-by-step instructions.

