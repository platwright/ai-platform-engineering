# Module 13 Concepts

## AI Extends The Attack Surface Beyond Web Applications

The OWASP Top 10 for web applications covers injection, broken authentication, sensitive data exposure, and similar threats. AI systems have all of those, plus a new class of threats that arise from the model's role in processing and acting on unstructured input.

The model is simultaneously a feature and an attack surface. It interprets text, and that interpretation can be manipulated.

## Prompt Injection Is The Central AI-Specific Threat

Prompt injection is an attack where malicious content in the input overrides the system instructions. It is structurally similar to SQL injection — both involve data being interpreted as instructions — but it is harder to prevent because language model interpretation is not rule-based. There is no grammar to enforce, no quoting mechanism that works universally, and no parser that can reliably separate instruction from data.

Defense requires layers: input validation, instruction privilege separation, output filtering, and authorization checks that do not trust model output.

## Tool Execution Turns Language Into Action

A language model that can only generate text is a low-risk system. A language model that can call APIs, delete records, execute code, or send messages has an attack surface proportional to the power of the tools it can invoke. Every tool added to an agent increases the blast radius of a successful injection or a misguided model decision.

The principle of least privilege applies: give agents access only to the tools they need for their defined purpose, not the full tool catalog.

## RAG Systems Are Data Systems With Access Control Requirements

A RAG system that ingests documents and returns them in response to queries has all the access control requirements of any data system, plus the risk that retrieved content will be executed as instructions by the downstream model.

Multi-tenant RAG requires explicit isolation: metadata filtering, tenant-scoped indexes, and authorization checks at retrieval time — not just at ingestion time.

## Secrets In AI Infrastructure Are Attractive Targets

Model API keys provide access to expensive compute capacity and potentially sensitive data. Vector database credentials provide access to knowledge bases that may contain proprietary information. These credentials are high-value targets and must be treated with the same rigor as database passwords or cloud provider credentials.

## Defense In Depth Is The Only Viable Strategy

No single control prevents all AI security threats. Prompt injection cannot be eliminated by any single mitigation. The correct response is layered defense: each layer catches what the previous layer misses.
