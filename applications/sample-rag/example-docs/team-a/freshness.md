# Retrieval Freshness

Platform teams should treat retrieval freshness as an operational property, not only as a data concern. If new documents are not ingested and re-indexed quickly enough, users can receive outdated answers even when the retrieval latency is low.

Freshness depends on ingestion pipelines, chunking logic, index update frequency, and failure handling during embedding generation.