# Chapter 02 - Authentication and Authorization for AI Workloads

## AuthN vs AuthZ In AI Platform Context

Authentication (AuthN) answers: who is making this request?
Authorization (AuthZ) answers: is this identity allowed to do this thing?

Both are necessary. An AI platform that authenticates users but does not enforce what each user can access, which models they can call, or which tools an agent can invoke has done half the work.

## Authentication Patterns

### API Key Authentication

The simplest approach for machine-to-machine calls and developer access:

```
Authorization: Bearer sk-platform-team-a-1234567890
```

API keys must be:
- unique per tenant or per application
- rotatable without service restart
- stored in a secrets manager, not in code or environment variables
- scoped (a key for team-a should not work for team-b)

### JWT Authentication

JSON Web Tokens carry claims about the caller's identity and scope. Suitable for user-facing requests and service-to-service calls within a trust boundary:

```json
{
  "sub": "user-123",
  "tenant": "team-a",
  "scope": ["model:read", "rag:query", "agent:run"],
  "exp": 1725220800
}
```

The AI gateway validates the JWT signature, extracts claims, and uses the `tenant` and `scope` claims for authorization decisions.

### Service Account Authentication (Kubernetes)

For Kubernetes-native deployments, workloads authenticate using service accounts and projected tokens:

```yaml
# The pod spec references a ServiceAccount
spec:
  serviceAccountName: ai-gateway
```

The service account token is projected into the pod and can be used for OIDC-based authentication with internal services.

## Authorization Patterns

### Role-Based Access Control (RBAC)

Define roles and bind them to identities:

| Role | Permissions |
|---|---|
| `ai-consumer` | Call gateway, query RAG |
| `ai-admin` | All consumer permissions + manage services |
| `ai-platform-ops` | All permissions |
| `agent-restricted` | Query RAG, read metrics (no destructive tools) |
| `agent-privileged` | All agent-restricted + destructive tools with approval |

### Scope-Based Authorization

More granular than roles; permissions are specific action + resource pairs:

```
model:read             → call any model endpoint
model:write:gpt-4o     → call specifically gpt-4o (tenant-level model access control)
rag:query              → query any RAG service
rag:query:team-a-kb    → query specifically team-a-kb
rag:ingest:team-a-kb   → ingest into team-a-kb
agent:run              → run agent objectives
agent:run:destructive  → run objectives that require destructive tools
```

Scope-based authorization is enforced at the gateway for model access and at the tool registry for agent tool access.

## Gateway-Level Authorization

The AI gateway is the best place to enforce model access control because it is the single point through which all model traffic flows:

```python
def authorize_model_request(request: dict, claims: dict) -> bool:
    tenant = claims["tenant"]
    requested_model = request.get("model", "default")
    
    # Check model access list for this tenant
    allowed_models = get_allowed_models(tenant)
    if requested_model not in allowed_models:
        log_policy_event(
            tenant=tenant,
            action="model_access_denied",
            requested=requested_model,
            allowed=allowed_models
        )
        return False
    return True
```

Model access policies may be needed when:
- some models are more expensive and only premium tenants can access them
- some models require data residency controls that restrict which tenants can use them
- some models are experimental and only accessible to specific teams

## Agent Identity And Scope Binding

Each agent run should have a stable identity bound to it at the start. This identity determines which tools the agent can access:

```python
class AgentContext:
    agent_id: str        # "rag-assistant-v2"
    tenant: str          # "team-a"
    allowed_tools: list  # ["query_rag", "get_metrics"]
    allow_destructive: bool  # False
    approval_required_for: list  # ["delete_rag_service", "scale_deployment"]
```

The tool registry enforces that tool calls match the agent context. The model cannot override this by producing a tool call to a tool not in `allowed_tools`.

## Zero-Trust Principles For Service-to-Service Calls

In a zero-trust architecture, service identity is verified even for internal calls. The agent platform calling the RAG platform should prove its identity, not just assert it:

- use mTLS for service-to-service calls in Kubernetes
- or use OIDC tokens issued by the Kubernetes service account mechanism
- never trust internal network location alone as proof of identity

This prevents lateral movement if one internal service is compromised.
