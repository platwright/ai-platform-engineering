# Chapter 05 - Agent Observability

## The Agent Observability Problem

Agents are harder to observe than conventional request-response services because:

- a single user request may trigger multiple model calls and multiple tool executions
- the agent's decision-making process (which tool to call and why) is implicit in model outputs
- tool calls have side effects that need to be auditable, not just measurable
- human approval events are part of the operational flow, not exceptions

An agent that makes three tool calls, including one that required approval, represents at least five distinct spans across three services. Without end-to-end tracing and explicit event logging, operators cannot reconstruct what happened.

## Agent-Level Spans

An agent run should produce a parent span covering the full execution, with child spans for each step:

```
agent.run (objective: "query RAG for team-a") [2,340ms]
├── llm.plan (model decision: which tool to call) [380ms]
├── tool.execute (tool: query_rag, service: team-a-kb) [140ms]
├── llm.generate (final response using tool result) [1,760ms]
└── artifact.write (run artifact saved) [60ms]
```

For a multi-step agent with approval:

```
agent.run (objective: "delete team-a-kb") [450ms]
├── llm.plan (model decision: delete_rag_service) [340ms]
├── approval.request (action: delete, service: team-a-kb) [5ms]
├── approval.decision (DENY, no approval token) [1ms]
└── artifact.write (blocked run saved) [60ms]
```

## Key Agent Metrics

| Metric | Description |
|---|---|
| `agent_run_total` | Total runs by tenant and objective type |
| `agent_run_duration_seconds` | End-to-end run duration |
| `agent_tool_calls_per_run` | Distribution of tool calls per run |
| `agent_tool_call_total` | Tool call count by tool name and status |
| `agent_tool_call_duration_seconds` | Tool execution latency by tool |
| `agent_approval_requests_total` | Approval requests by action type |
| `agent_approval_decisions_total` | Approvals granted and denied |
| `agent_loop_depth` | Number of model iterations before final response |
| `agent_cost_usd_total` | Estimated cost per run by tenant |

## Tool Call Observability

Each tool call should produce structured event data:

```json
{
  "event": "tool_call",
  "timestamp": "2025-09-01T14:32:15Z",
  "trace_id": "abc123",
  "agent_run_id": "run-789",
  "tool_name": "query_rag",
  "arguments": {
    "service_name": "team-a-kb",
    "question": "What is retrieval freshness?"
  },
  "result_status": "success",
  "result_preview": "Retrieval freshness refers to...",
  "duration_ms": 140,
  "authorized": true
}
```

The `authorized` field distinguishes successful tool calls from unapproved attempts. Even blocked attempts should be logged with the full argument set, as they are potential security events.

## Approval Event Observability

Human-in-the-loop approval events require special attention. An approval event log entry should contain:

```json
{
  "event": "approval_decision",
  "timestamp": "2025-09-01T14:32:20Z",
  "trace_id": "abc123",
  "agent_run_id": "run-789",
  "action": "delete_rag_service",
  "arguments": {"service_name": "team-a-kb"},
  "decision": "DENY",
  "reason": "no approval token provided",
  "approver_identity": null
}
```

When the decision is `GRANT`, the `approver_identity` field records who authorized the action. This is the audit trail that satisfies security and compliance requirements.

## Alerting On Agent Behavior

Standard rate and latency alerts apply to agent workloads. AI-specific alerts:

| Alert | Condition | Severity |
|---|---|---|
| High tool error rate | `tool_call_errors / total_tool_calls > 0.10` | High |
| Approval bypass attempt | Any tool call with `authorized=false` that executed | Critical |
| High loop depth | `agent_loop_depth > 10` on any run | Warning |
| Approval rate spike | Unusual increase in approval requests | Medium |
| Agent cost spike | `agent_cost_usd_total` rate doubles | High |

The "approval bypass attempt" alert is a security alert, not just an operational one. A tool execution that bypassed the authorization gate should trigger immediate investigation.

## Run Artifacts As Observability

Agent run artifacts (the JSON output files from Project 04) are a form of structured observability data. They should be:

- stored in an accessible location indexed by agent session and timestamp
- indexed for search by objective type, tool calls made, and outcome
- retained for the same duration as access logs (typically 90 days minimum)
- available to both the platform team for debugging and the security team for audit

Run artifacts complement traces by providing a human-readable narrative of the agent's decision process, which raw spans do not always convey clearly.
