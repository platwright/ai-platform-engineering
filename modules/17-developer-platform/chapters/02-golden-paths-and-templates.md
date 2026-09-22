# Chapter 02 - Golden Paths and Templates

## What A Golden Path Is

A golden path is a well-supported, recommended way to accomplish a common task on the platform. The term comes from the idea that the path is paved — it is smooth, well-maintained, and the obvious route. Other paths exist but require more effort.

A golden path is:
- **Opinionated**: it makes specific choices so developers do not have to
- **Validated**: it produces working, compliant applications by construction
- **Maintained**: it is updated when the platform evolves
- **Well-documented**: the rationale for each choice is explained

A golden path is not:
- a mandate that prevents other approaches
- a checklist that developers must manually verify
- a document that describes what a developer should produce

The defining characteristic: using the golden path is easier than not using it.

## The AI Application Golden Paths

For the Acme AI platform, the common golden paths are:

| Path Name | Use Case | What It Produces |
|---|---|---|
| `ai-chat-app` | Simple chatbot or assistant | App with gateway integration, prompt template, logging |
| `ai-rag-app` | Document Q&A application | App with gateway + RAG service, ingestion pipeline |
| `ai-agent-app` | Automation with tool use | App with agent platform, tool definitions, approval config |
| `rag-service-onboarding` | Register a new RAG knowledge base | Service catalog entry, ingestion job, access policy |

## Template Structure

Each golden path is a scaffolding template that produces a complete, working starting point:

```
ai-rag-app/
├── app.py                    ← working application with gateway + RAG integration
├── config/
│   └── app.example.json      ← complete configuration with sensible defaults
├── prompts/
│   └── rag-grounding.yaml    ← versioned system prompt template
├── eval/
│   └── smoke-cases.json      ← 10 starter evaluation cases
├── .github/workflows/
│   └── eval.yml              ← CI pipeline: lint + smoke eval on every PR
├── Dockerfile                ← container image definition
├── README.md                 ← generated README with team and purpose filled in
└── docs/
    └── runbook.md            ← incident runbook template
```

A developer who uses this template gets a working application on day one. They do not need to understand CI pipeline configuration, Dockerfile best practices, or prompt versioning conventions — those are embedded in the template.

## Template Design Principles

### Compile-Time Correctness

Templates should produce applications that work without modification, not applications that need to be debugged before they work. Every template should be tested end-to-end before it is published.

### Encode Best Practices, Not Just Examples

A template that omits the CI pipeline because "teams will add their own" defeats the purpose. Best practices — evaluation gates, observability hooks, secret management patterns — should be present by default.

### Make Customization Discoverable

Templates should be easy to customize. Comments in generated files should explain what can be changed and why. Common customization points should be highlighted in the README.

### Version And Deprecate Templates

Templates need maintenance. When the platform evolves (new model tier, new gateway API version, new secret management approach), templates need updating. Track template versions and communicate deprecations to teams using old versions.

## Template Parameters

Templates take parameters that customize the generated output:

```yaml
# Backstage scaffolder template parameters
parameters:
  - title: Application Details
    properties:
      appName:
        type: string
        title: Application Name
      teamName:
        type: string
        title: Your Team Name
      ragServiceName:
        type: string
        title: RAG Service Name
        description: The name of the RAG service your app will use
      modelTier:
        type: string
        title: Model Tier
        enum: [standard, premium]
        default: standard
        description: standard uses gpt-4o-mini; premium uses gpt-4o
```

Parameters become variables in the generated files. The developer fills in the form; the template does the rest.

## Keeping Templates Current

The most common failure mode for golden paths is staleness. A template that still references a deprecated API version, an old model name, or a removed configuration format produces broken applications and damages trust in the platform.

Assign template ownership. When the platform changes, the owner updates the relevant templates before the change goes live in production. This is the same discipline as maintaining a dependency.
