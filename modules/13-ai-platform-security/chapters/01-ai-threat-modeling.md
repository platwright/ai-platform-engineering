# Chapter 01 - AI Threat Modeling

## Why AI Systems Need A Separate Threat Model

Conventional threat modeling for web applications addresses well-understood attack classes: injection, broken authentication, insecure deserialization, supply chain. AI systems have all of these, plus a fundamentally new category: threats that arise from the model's interpretation of unstructured natural language.

A traditional security boundary is binary — a request either has the right credentials or it does not. AI systems have a fuzzy boundary: the model may be convinced to behave differently by the content of the input, regardless of whether the requester is authenticated.

## STRIDE Applied To AI Systems

STRIDE is a widely-used threat modeling framework that identifies six threat categories:

| Category | Definition | AI-Specific Example |
|---|---|---|
| **S**poofing | Claiming a false identity | Agent claims to be a system process to gain elevated tool access |
| **T**ampering | Modifying data in transit or storage | Poisoning the RAG index with malicious documents |
| **R**epudiation | Denying an action was taken | No audit trail for which agent called which tool |
| **I**nformation disclosure | Exposing private information | Model extracts PII from a retrieval result and echoes it |
| **D**enial of service | Making a service unavailable | Sending extremely long prompts to exhaust context window capacity |
| **E**levation of privilege | Gaining unauthorized capabilities | Prompt injection overrides system instructions to call restricted tools |

## OWASP LLM Top 10

The OWASP Top 10 for Large Language Model Applications provides a focused threat taxonomy for AI systems:

| ID | Threat | Brief Description |
|---|---|---|
| LLM01 | Prompt Injection | Manipulating model behavior through crafted input |
| LLM02 | Sensitive Information Disclosure | Model reveals private training data or system prompts |
| LLM03 | Supply Chain | Compromised models, plugins, or dependencies |
| LLM04 | Data and Model Poisoning | Training or fine-tuning data contamination |
| LLM05 | Improper Output Handling | Unsafe downstream processing of model output |
| LLM06 | Excessive Agency | Over-privileged model actions via tools |
| LLM07 | System Prompt Leakage | Extraction of system prompt contents |
| LLM08 | Vector and Embedding Weaknesses | Attacks on the RAG retrieval pipeline |
| LLM09 | Misinformation | Convincingly wrong outputs presented as facts |
| LLM10 | Unbounded Consumption | Resource exhaustion via unconstrained generation |

This module covers LLM01, 02, 03, 04, 06, 07, 08, and the platform controls for each.

## Threat Modeling The Acme AI Platform

Apply STRIDE to each component:

### AI Gateway

| Threat | Specific Risk | Control |
|---|---|---|
| Spoofing | Tenant ID forging in request headers | JWT authentication, do not trust client-provided tenant IDs |
| Tampering | Routing configuration modification | Config versioning, access control on gateway config |
| Info Disclosure | Model API keys in gateway logs | Log scrubbing, structured logging with secrets omitted |
| DoS | Token flood from one tenant | Rate limiting per tenant |
| Elevation | Tenant A accessing Tenant B routes | Strict tenant scope enforcement in routing logic |

### RAG Platform

| Threat | Specific Risk | Control |
|---|---|---|
| Tampering | Malicious document injected into index | Ingestion validation, content review for sensitive tenants |
| Info Disclosure | Tenant B retrieving Tenant A documents | Metadata filtering enforcement at query time |
| Info Disclosure | PII in vector store returned in responses | Data classification before ingestion |
| Elevation | Indirect prompt injection via retrieved document | Output filtering, privilege separation in system prompt |

### Agent Platform

| Threat | Specific Risk | Control |
|---|---|---|
| Elevation | Model calls destructive tool without approval | Approval gates, tool scope policy |
| Spoofing | Crafted objective makes agent act as different identity | Agent identity binding at request time |
| Repudiation | No record of which tool was called | Mandatory tool call audit logging |
| DoS | Agent loop never terminates | Loop depth limit, timeout enforcement |

## Asset Inventory

Before building controls, identify what you are protecting:

| Asset | Classification | Why It Matters |
|---|---|---|
| Model API keys | Secret | Access to inference capacity and billing |
| Vector database credentials | Secret | Access to all indexed knowledge |
| RAG index data | Confidential | May contain proprietary or sensitive documents |
| Agent run artifacts | Internal | Contain tool call arguments and decision history |
| System prompts | Confidential | Reveal platform architecture and can be exploited |
| User conversation history | PII-possible | May contain identifiable user information |
| Eval datasets | Internal | May contain sensitive test cases |

## Threat Model Output

A threat model for the AI platform should produce:

1. A list of threats ranked by likelihood × impact
2. A list of controls for each high and critical threat
3. A list of accepted risks (threats where the cost of control exceeds the risk)
4. A list of open questions requiring further investigation

The threat model is a living document. Revisit it when new capabilities (new tools, new models, new tenants) are added to the platform.
