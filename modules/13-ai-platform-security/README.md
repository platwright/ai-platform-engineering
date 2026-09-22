# Module 13 - AI Platform Security

## Overview

AI systems introduce security concerns that sit outside the typical OWASP web application threat model. Prompt injection, model supply chain attacks, insecure tool execution, RAG data poisoning, and inference-time data exfiltration are real threats in production AI platforms.

This module builds a threat model specific to AI platform workloads and maps concrete controls to each threat category. The emphasis is on platform engineering concerns — authorization, secrets management, network policy, audit logging — not adversarial ML research.

## Learning Objectives

By the end of this module, you should be able to:

- build a threat model for an AI platform using STRIDE and the OWASP LLM Top 10
- apply authentication and authorization patterns appropriate to AI workload surfaces
- manage secrets for model API keys, embedding services, and vector database credentials
- explain prompt injection as a platform defense problem with layered controls
- describe the attack surface of tool-calling agents and the controls that mitigate each risk
- apply security boundaries to multi-tenant RAG systems
- reason about model supply chain risks and mitigation approaches
- implement audit logging requirements for a security incident investigation

## Prerequisites

- Completion of [modules/12-observability/README.md](../12-observability/README.md)
- Familiarity with basic network security concepts (TLS, tokens, network policies)
- Completion of Projects 01 through 04

## Difficulty And Time

- Difficulty: Advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [AI Threat Modeling](chapters/01-ai-threat-modeling.md)
2. [Authentication and Authorization for AI Workloads](chapters/02-authentication-and-authorization.md)
3. [Secrets Management for Model Infrastructure](chapters/03-secrets-management.md)
4. [Prompt Injection](chapters/04-prompt-injection.md)
5. [Tool and Agent Security](chapters/05-tool-and-agent-security.md)
6. [RAG Security and Data Boundaries](chapters/06-rag-security-and-data-boundaries.md)
7. [Model Supply Chain Security](chapters/07-model-supply-chain-security.md)
8. [Audit Logging for AI Systems](chapters/08-audit-logging-for-ai-systems.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

## Expected Outcome

At the end of this module, you should have:

- a documented threat model for the Acme AI platform
- a concrete understanding of how prompt injection works and why it cannot be fully prevented
- an audit of the sample application stack's current security posture
- notes on which controls are most critical to add first

## Knowledge Check

1. Apply STRIDE to the AI gateway: what threats does each letter represent at this component?
2. Why is prompt injection a harder problem than SQL injection even though they are structurally similar?
3. What is the difference between direct prompt injection and indirect prompt injection via RAG?
4. Why does giving an agent access to a `delete_service` tool without approval gates create a security risk beyond normal API security?
5. Where should model API keys be stored in a production Kubernetes deployment, and where should they never be stored?
6. What information must a security audit log entry contain for an agent tool call to be useful during an incident investigation?
7. What is a "confused deputy attack" in the context of multi-agent systems?

## Common Mistakes

- treating prompt injection as purely a prompt engineering problem and not a platform defense problem
- storing model API keys in environment variables in Kubernetes without a secrets manager
- logging full prompt and response content without scrubbing or access controls
- giving agents broad tool access "for convenience" without a least-privilege policy
- assuming open-weight model weights are safe because they are popular
- building RAG systems where one tenant's query could theoretically return another tenant's documents

## Production Considerations

- defense in depth: no single control is sufficient; prompt injection requires input filtering, system prompt hardening, output filtering, and tool authorization working together
- secrets rotation: model API keys should be rotatable without application redeployment
- RAG authorization: every retrieval result should carry the access permissions of the document it came from
- agent audit trails: tool calls, approvals, and denials must be retained as security records, not just operational logs
- supply chain: every open-weight model deployed should have its origin and integrity verified

## Next Step

Read [concepts.md](concepts.md), then work through the threat modeling and security audit exercises in [lab.md](lab.md).