# Chapter 05 - Tool and Agent Security

## The Excessive Agency Problem

OWASP LLM06 describes "Excessive Agency" as the risk that a language model is given too much capability to take actions in the world. This is not a theoretical concern — every tool you add to an agent is a real capability that a successful injection or a model error can invoke.

The question is not "what tools would be useful?" but "what is the minimum set of tools this agent needs for its defined purpose, and what is the worst thing it can do with those tools?"

## Principle Of Least Privilege For Tool Scopes

Every agent deployment should have an explicit tool scope:

```python
# WRONG: agent can call everything
agent_tools = tool_registry.get_all_tools()

# RIGHT: agent can only call tools appropriate to its purpose
agent_tools = tool_registry.get_tools(
    allowed=["query_rag", "get_service_health", "get_metrics"]
)
```

Tool scopes should be defined at deployment time and enforced by the tool registry. The model cannot override them by producing a tool call to an out-of-scope tool.

## Tool Schema Validation

Tool call arguments provided by the model must be validated before execution:

```python
def execute_tool(tool_name: str, arguments: dict, agent_ctx: AgentContext) -> dict:
    # 1. Check tool is in scope
    if tool_name not in agent_ctx.allowed_tools:
        raise AuthorizationError(f"Tool {tool_name} not in agent scope")
    
    # 2. Validate arguments against schema
    tool_def = tool_registry.get(tool_name)
    try:
        jsonschema.validate(arguments, tool_def["parameters"])
    except jsonschema.ValidationError as e:
        raise ValueError(f"Invalid tool arguments: {e.message}")
    
    # 3. Check for path traversal, injection, and other input attacks
    for field, value in arguments.items():
        if isinstance(value, str) and (".." in value or ";" in value):
            raise ValueError(f"Suspicious characters in argument {field}")
    
    # 4. Execute
    return tool_def["handler"](**arguments)
```

## Approval Gates For Destructive Actions

Destructive, irreversible, or high-impact tool calls must require an explicit approval token:

```python
REQUIRES_APPROVAL = {
    "delete_rag_service",
    "scale_deployment_to_zero",
    "revoke_api_key",
    "send_notification_to_all_users",
}

def check_approval(tool_name: str, agent_ctx: AgentContext, approval_token: str | None) -> bool:
    if tool_name not in REQUIRES_APPROVAL:
        return True
    if approval_token is None:
        return False
    # Validate token format, expiry, and scope
    return validate_approval_token(approval_token, tool_name, agent_ctx.tenant)
```

The approval token should be:
- generated out-of-band (not by the model)
- scoped to a specific action and tenant
- time-limited (expires within minutes)
- single-use where possible

## Sandboxing Code Execution Tools

If any agent tool executes code (a Python interpreter, a shell command, a database query), that tool must be sandboxed:

- run in a separate container with minimal privileges
- no network access to internal services
- no access to secrets or credentials
- CPU and memory limits enforced
- execution timeout enforced
- output captured and inspected before returning to agent

Code execution without sandboxing is a remote code execution vulnerability, regardless of how it is framed in the product.

## The Confused Deputy Problem In Multi-Agent Systems

A confused deputy attack occurs when a less-trusted agent tricks a more-trusted agent or service into taking an action it should not take on the attacker's behalf.

Example in AI systems:

1. An agent with broad tool access accepts objectives from external users
2. A user crafts an objective that, when processed, causes the agent to call a high-privilege tool it would not normally call for this user
3. The tool executes with the agent's credentials (not the user's), bypassing the user's access controls

Mitigations:
- bind tool scope to the least-privileged identity in the chain (the user, not the agent)
- agent identity should not have broader access than the user who initiated the objective
- approval for destructive actions should come from the user's identity, not the agent's

## Loop Depth And Timeout Limits

Agents that loop indefinitely create a denial of service risk:

```python
MAX_LOOP_DEPTH = 10
AGENT_TIMEOUT_SECONDS = 120

def run_agent_loop(objective: str, ctx: AgentContext) -> dict:
    history = []
    depth = 0
    start = time.time()
    
    while depth < MAX_LOOP_DEPTH:
        if time.time() - start > AGENT_TIMEOUT_SECONDS:
            raise TimeoutError("Agent loop exceeded time limit")
        
        response = call_model(messages=history + [{"role": "user", "content": objective}])
        
        if not response.tool_calls:
            return {"response": response.content, "loop_depth": depth}
        
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call.name, tool_call.arguments, ctx)
            history.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
        
        depth += 1
    
    raise RuntimeError(f"Agent loop depth exceeded {MAX_LOOP_DEPTH}")
```

Both limits should produce logged events, not silent failures.

## Audit Trail Requirements

Every tool call must be logged with sufficient detail to reconstruct what happened during a security investigation:

```json
{
  "event_type": "tool_call",
  "timestamp": "2025-09-01T14:32:15Z",
  "agent_run_id": "run-789",
  "agent_id": "rag-assistant-v2",
  "tenant": "team-a",
  "tool_name": "query_rag",
  "arguments": {"service_name": "team-a-kb", "question": "What is..."},
  "authorized": true,
  "approval_token": null,
  "result_status": "success",
  "duration_ms": 140
}
```

For denied or suspicious calls:

```json
{
  "event_type": "tool_call_denied",
  "timestamp": "...",
  "tool_name": "delete_rag_service",
  "reason": "no_approval_token",
  "severity": "security_alert"
}
```

These records are security artifacts. Retain them for 90 days minimum and ensure they are tamper-evident.
