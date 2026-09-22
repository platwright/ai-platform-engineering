# Chapter 08 - Audit Logging for AI Systems

## What AI Audit Logging Requires

An audit log exists to answer questions during a security investigation: what happened, who did it, when, and to what? For AI systems, the questions extend to: what did the model produce, which tools were called, was approval obtained, and what data was retrieved?

Standard HTTP access logs answer only a small fraction of these questions. AI audit logs must go deeper.

## What To Log

### Model Invocations

```json
{
  "event_type": "model_invocation",
  "timestamp": "2025-09-01T14:32:10Z",
  "request_id": "req-abc123",
  "session_id": "sess-xyz789",
  "tenant": "team-a",
  "user_identity": "user-001",
  "model": "gpt-4o-mini-2024-07-18",
  "prompt_version": "rag-grounding-v1.4.0",
  "prompt_tokens": 843,
  "completion_tokens": 142,
  "finish_reason": "stop",
  "latency_ms": 1834,
  "cost_usd": 0.000714,
  "ip_address": "192.168.1.50"
}
```

Note what is intentionally absent: full prompt text and full response text. These may contain PII or sensitive content. Include them only if you have explicit authorization and appropriate access controls on the audit log store.

### Tool Calls

```json
{
  "event_type": "tool_call",
  "timestamp": "2025-09-01T14:32:15Z",
  "request_id": "req-abc123",
  "agent_run_id": "run-789",
  "agent_id": "rag-assistant-v2",
  "tenant": "team-a",
  "tool_name": "query_rag",
  "arguments": {
    "service_name": "team-a-kb",
    "question": "What is retrieval freshness?"
  },
  "authorized": true,
  "approval_token_id": null,
  "result_status": "success",
  "duration_ms": 140
}
```

### Authorization Events (All Outcomes)

```json
{
  "event_type": "authorization",
  "timestamp": "...",
  "request_id": "req-abc124",
  "tenant": "team-b",
  "resource": "model:gpt-4o",
  "action": "invoke",
  "decision": "denied",
  "reason": "model_not_in_tenant_allowlist",
  "severity": "informational"
}
```

### Security Events (Elevated Severity)

```json
{
  "event_type": "security_event",
  "timestamp": "...",
  "severity": "high",
  "category": "suspected_prompt_injection",
  "request_id": "req-abc125",
  "tenant": "team-c",
  "detection_pattern": "ignore_previous_instructions",
  "input_preview": "ignore all previous instruct...",
  "action_taken": "blocked"
}
```

Security events should have elevated retention and separate access controls from operational logs.

## What NOT To Log (Without Controls)

The following should be logged only with appropriate authorization, scrubbing, and access control:

- full prompt text (may contain PII, confidential queries, system prompt details)
- full response text (may contain PII, sensitive retrieved content)
- user-uploaded document content
- raw conversation history

If you do log sensitive content, enforce:
- dedicated log store with restricted access (not the general ops log store)
- encryption at rest
- defined retention period (90 days or as required by regulation)
- PII scrubbing before any human review

## Log Integrity

Audit logs are only useful for security investigations if they can be trusted. Log tampering is a meaningful risk when investigating insider threats.

Controls:
- **Write-once storage**: configure the audit log store to reject modifications to existing entries
- **Centralized log forwarding**: forward logs to an external SIEM or log management system that the application server cannot write to
- **Hash chaining**: each log entry includes a hash of the previous entry, enabling tamper detection

## Retention Policies

Different log categories have different retention requirements:

| Log Type | Minimum Retention | Rationale |
|---|---|---|
| Security events | 12 months | Security investigation, compliance |
| Tool call audit logs | 6 months | Incident investigation |
| Model invocation metadata | 90 days | Cost audit, quality investigation |
| Operational request logs | 30 days | Debugging |
| Full prompt/response content | 30 days | With scrubbing and access controls |

These are minimums. Regulated industries (finance, healthcare, legal) may require longer retention periods.

## SIEM Integration

Security audit events should flow to a Security Information and Event Management (SIEM) system:

```yaml
# Fluent Bit config for forwarding security events to SIEM
[FILTER]
    Name     grep
    Match    ai-platform.*
    Regex    event_type security_event|tool_call_denied|authorization

[OUTPUT]
    Name     http
    Match    ai-platform.*
    Host     siem.internal
    Port     514
    URI      /api/events
    Format   json_lines
```

SIEM rules to create for AI platforms:
- Alert when `security_event.category == "suspected_prompt_injection"` rate exceeds threshold
- Alert on any `tool_call` with `authorized = false` that completed (bypass)
- Alert when a tenant's model invocation rate doubles within an hour (credential compromise indicator)
- Alert when `authorization.decision == "denied"` rate for a single tenant exceeds threshold (credential stuffing)

## Incident Investigation Using Audit Logs

When an incident occurs, the audit log enables a structured investigation:

```bash
# 1. Find all events for a suspicious session
jq 'select(.session_id == "sess-xyz789")' audit.log | sort_by(.timestamp)

# 2. Find all tool calls in a time window
jq 'select(.event_type == "tool_call" and .timestamp > "2025-09-01T14:00:00Z")' audit.log

# 3. Find all authorization denials for a tenant
jq 'select(.event_type == "authorization" and .decision == "denied" and .tenant == "team-c")' audit.log

# 4. Find all high-severity security events
jq 'select(.event_type == "security_event" and .severity == "high")' audit.log
```

The ability to answer these queries quickly is the measure of a functional audit log implementation. Test this before an incident, not during one.
