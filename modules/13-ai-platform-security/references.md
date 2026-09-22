# Module 13 References

## AI Security Frameworks

- [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — the primary AI security threat taxonomy
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial threat landscape for AI systems
- [NIST AI Risk Management Framework](https://www.nist.gov/system/files/documents/2023/01/26/NIST-AI-600-1.pdf) — government AI risk management guidance

## Prompt Injection

- [Prompt Injection Attacks Against GPT-3 (Riley Goodside)](https://simonwillison.net/2022/Sep/12/prompt-injection/) — original framing of prompt injection as a security concern
- [Not What You've Signed Up For (Greshake et al.)](https://arxiv.org/abs/2302.12173) — indirect prompt injection paper
- [Prompt Injection Primer for Engineers](https://github.com/jthack/PIPE) — practical guide to prompt injection patterns
- [AI Injection Defense Patterns](https://learnprompting.org/docs/prompt_hacking/defense) — overview of defense approaches

## Authentication and Authorization

- [OAuth 2.0 Security Best Practices (RFC 9700)](https://www.rfc-editor.org/rfc/rfc9700) — current JWT/OAuth security guidance
- [Kubernetes RBAC Documentation](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) — Kubernetes authorization reference
- [Zero Trust Architecture (NIST SP 800-207)](https://csrc.nist.gov/publications/detail/sp/800-207/final) — zero trust design principles

## Secrets Management

- [HashiCorp Vault](https://developer.hashicorp.com/vault) — open-source secrets management
- [External Secrets Operator](https://external-secrets.io/) — Kubernetes native secrets synchronization
- [Kubernetes Secrets Encryption at Rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) — encrypting etcd-stored secrets

## Model Supply Chain

- [SafeTensors Repository](https://github.com/huggingface/safetensors) — safe model serialization format
- [Hugging Face Security Best Practices](https://huggingface.co/docs/hub/security) — model hub security guidance
- [ML Supply Chain Security (CNCF)](https://www.cncf.io/blog/2024/02/07/securing-the-ml-supply-chain/) — supply chain security for ML artifacts

## RAG Security

- [Indirect Prompt Injection in RAG Systems](https://arxiv.org/abs/2311.11538) — research on RAG-specific injection risks
- [Poisoning Retrieval Corpora](https://arxiv.org/abs/2310.19156) — data poisoning for RAG attacks

## Audit Logging

- [OpenTelemetry Security Events](https://opentelemetry.io/docs/specs/semconv/general/events/) — event semantic conventions
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) — security-focused logging guidance
- [SIEM Integration Patterns](https://www.elastic.co/guide/en/siem/guide/current/index.html) — Elastic SIEM for security event analysis
