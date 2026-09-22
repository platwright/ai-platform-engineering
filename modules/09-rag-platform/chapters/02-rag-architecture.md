# Chapter 9.2 - RAG Architecture

A RAG system has two major paths:

- ingestion path: documents, chunking, embeddings, storage
- query path: query embedding, retrieval, reranking, grounded generation

Treating both as platform concerns makes the system easier to operate and reason about.