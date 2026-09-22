# Chapter 03 - Secrets Management for Model Infrastructure

## What Counts As A Secret In AI Infrastructure

AI infrastructure has a broader secrets surface than typical web services:

| Secret | Risk If Exposed |
|---|---|
| Model API keys (OpenAI, Anthropic, etc.) | Unauthorized inference charges, data access |
| Embedding service credentials | Unauthorized embedding generation, data exposure |
| Vector database credentials | Full access to all indexed knowledge |
| Model registry credentials | Access to proprietary fine-tuned model weights |
| Evaluation service API keys | Access to eval infrastructure and test data |
| Monitoring credentials | Access to operational telemetry |

Model API keys are especially attractive because they have direct monetary value (inference spend) and can be used to exfiltrate data by sending malicious prompts through someone else's account.

## Common Mistakes

### Secrets in Environment Variables (Without A Manager)

```yaml
# WRONG: secret visible to anyone with kubectl access to the pod spec
env:
  - name: OPENAI_API_KEY
    value: "sk-proj-real-secret-key-here"
```

Kubernetes environment variables are stored in the API server etcd and visible to any user with `kubectl describe pod` access.

### Secrets in Config Files Committed to Git

```json
{
  "model_api_key": "sk-real-secret-key",
  "model_api_url": "https://api.openai.com"
}
```

Even if the repository is private, secrets in code or config files:
- appear in git history even after deletion
- are accessible to anyone with repository access
- are included in build artifacts
- are not rotatable without a code change

### Secrets in Application Logs

```python
# WRONG: secret appears in logs
logger.info(f"Calling API with key {api_key}")
```

Log aggregation systems often have broader access than the application itself.

## Correct Approaches

### Kubernetes Secrets With RBAC

Kubernetes Secrets are base64-encoded (not encrypted at rest by default, but can be). Combined with RBAC:

```yaml
# Secret definition
apiVersion: v1
kind: Secret
metadata:
  name: model-api-credentials
  namespace: ai-platform
type: Opaque
stringData:
  OPENAI_API_KEY: "sk-real-key-goes-here"

---
# Reference in pod spec
env:
  - name: OPENAI_API_KEY
    valueFrom:
      secretKeyRef:
        name: model-api-credentials
        key: OPENAI_API_KEY
```

Restrict access with RBAC:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: ai-platform
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["model-api-credentials"]
    verbs: ["get"]
```

Enable encryption at rest in your cluster to protect secrets in etcd.

### External Secrets Operator

For production, use an External Secrets Operator that syncs secrets from a vault:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: model-api-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: model-api-credentials
  data:
    - secretKey: OPENAI_API_KEY
      remoteRef:
        key: ai-platform/openai
        property: api_key
```

This pattern:
- stores secrets in HashiCorp Vault, AWS Secrets Manager, or GCP Secret Manager
- automatically rotates them into Kubernetes Secrets
- enables audit logging of secret access
- allows rotation without any application code change

### Secret Rotation

Model API keys should be rotatable on a defined schedule or on demand:

1. Generate a new key at the provider
2. Update the secret in the vault
3. The External Secrets Operator syncs the new value to Kubernetes
4. The application picks up the new key on next request (or pod restart for env vars)
5. Revoke the old key at the provider

With environment-variable-based secrets, step 4 requires a pod restart. With secrets fetched per-request from a vault client library, rotation is seamless.

## Log Scrubbing

Audit every log path for secret leakage:

```python
import re

SECRET_PATTERNS = [
    (r'sk-[a-zA-Z0-9]{32,}', 'OPENAI_KEY_REDACTED'),
    (r'Bearer [a-zA-Z0-9._-]{20,}', 'BEARER_TOKEN_REDACTED'),
    (r'"api_key"\s*:\s*"[^"]{8,}"', '"api_key": "REDACTED"'),
]

def scrub_secrets(text: str) -> str:
    for pattern, replacement in SECRET_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text
```

Run scrubbing in the log handler, not in the application code that generates the log. The handler is the safety net; the application should not be generating log lines with secrets in the first place.

## Secret Scope Minimization

Each service should have access only to the secrets it needs:

| Service | Needs |
|---|---|
| AI Gateway | Model provider API keys, gateway own signing key |
| RAG Platform | Embedding service key, vector DB credentials |
| Agent Platform | Tool execution credentials (per-tool scoped) |
| Eval Runner | Model API key for judge calls, eval dataset access |

No single service should have access to all secrets. If the gateway is compromised, the vector DB credentials should not also be exposed.
