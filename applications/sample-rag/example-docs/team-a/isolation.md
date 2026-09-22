# Tenant Isolation

Multi-tenant RAG platforms need explicit tenant boundaries. Retrieval should filter candidate chunks by tenant or access scope before ranking results. If filtering happens too late or not at all, one team can receive another team's content.

Isolation therefore depends on metadata discipline, permissions, and consistent enforcement throughout ingestion and query paths.