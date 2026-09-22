# Project 03 Concepts

## Service Catalog

RAG-as-a-service begins with an explicit service catalog. Each service should declare:

- tenant or scope
- source document location or ingestion contract
- retrieval configuration
- platform-facing identifiers

## Managed Ingestion

Application teams should not need to re-implement chunking and index lifecycle logic in every app. The platform service owns ingestion workflows and index state.

## Tenant Isolation

The platform must make tenant boundaries explicit in storage and query behavior. That is why each service here owns a separate index file and named configuration.

## Contract Over Convenience

Project 03 prefers explicit service creation and explicit query endpoints because platform capabilities need contracts, not hidden magic.