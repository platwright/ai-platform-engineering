# Module 13 Challenge

## Challenge 1 - Threat Model

Build a STRIDE threat model for the AI gateway component.

For each of the six STRIDE categories, write:
1. One concrete threat relevant to the AI gateway
2. The likelihood (High/Medium/Low) and impact (High/Medium/Low)
3. The primary mitigating control
4. Whether the current local implementation has this control

Present your results as a table in `my-solutions/module-13-threat-model.md`.

## Challenge 2 - Prompt Injection Defense Layer

Implement a basic input validation function that detects common prompt injection patterns. The function should:

1. Accept a string input
2. Check against a list of pattern definitions (at least 8 patterns)
3. Return a tuple of `(is_suspicious: bool, matched_patterns: list[str])`
4. Log the detection with the matched patterns and a severity level

Test it against:
- Five obvious injection attempts from the OWASP examples
- Five normal user queries that should not trigger false positives

Document your false positive rate and explain why zero false positives is impossible without also missing real attacks.

## Challenge 3 - Secrets Management Improvement

Rewrite the sample application stack to load model API credentials from environment variables rather than config files, and document how this would be upgraded to use Kubernetes Secrets in production.

The documentation should cover:
1. The current approach and its risks
2. The environment variable approach (as an interim step)
3. The Kubernetes Secret approach
4. The External Secrets Operator approach (production target)

For each approach, describe the specific secret rotation procedure.

## Challenge 4 - RAG Indirection Attack

Design an indirect prompt injection attack against the sample-rag system using a malicious document. Write the attack document content in `my-solutions/module-13-injection-poc.txt`.

The attack document should attempt to:
- Override the system prompt's answer behavior
- Extract or echo information from the context

Then design a defense: write a document content scanner function that would detect this document before ingestion.

Note: This is an educational exercise. The purpose is to understand the attack surface, not to attack real systems.

## Challenge 5 - Audit Log Schema

Design a complete audit log schema for the Acme AI platform.

The schema should cover:
- 5 event types (choose from the chapter material or design your own)
- For each event type: all required fields, all optional fields, the severity level
- A data retention policy for each event type
- A sample SIEM query that would detect a meaningful threat using this schema

Write the schema as structured JSON Schema definitions in `my-solutions/module-13-audit-schema.json`.
