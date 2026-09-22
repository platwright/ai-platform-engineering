# Chapter 04 - Tool Calling

## What Tool Calling Is

Tool calling (also called function calling) is the mechanism by which a language model can request that an external function or API be executed on its behalf.

The model does not execute code itself. It outputs a structured request describing which tool to call and with what arguments. The calling system executes the tool and returns the result. The model then continues generation with the result in context.

```
User: "What is the current request error rate for the inference gateway?"
         |
         v
Model decides: I need to call get_metrics(service="inference-gateway", metric="error_rate")
         |
         v
Platform calls the actual metrics API
         |
         v
Result is added to the context: {"error_rate": 0.012, "window": "5m"}
         |
         v
Model generates: "The current 5-minute error rate for the inference gateway is 1.2%."
```

## The Tool Calling Protocol

Tool definitions are passed to the model in the request:

```json
{
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_service_metrics",
        "description": "Retrieve current metrics for a named platform service.",
        "parameters": {
          "type": "object",
          "properties": {
            "service_name": {
              "type": "string",
              "description": "The name of the platform service to query."
            },
            "metric": {
              "type": "string",
              "enum": ["error_rate", "latency_p50", "latency_p99", "request_count"],
              "description": "The metric to retrieve."
            },
            "window": {
              "type": "string",
              "description": "Time window, e.g. '5m', '1h', '24h'."
            }
          },
          "required": ["service_name", "metric"]
        }
      }
    }
  ]
}
```

When the model decides to call a tool, the response contains a `tool_calls` field instead of a text `content` field.

The calling system is then responsible for:
1. Parsing the tool call
2. Executing the real function
3. Returning the result to the model in a `tool` role message
4. Resuming model generation

## The Tool Call Loop

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. User message + tool definitions → model                                  │
│ 2. Model responds with tool_calls (or text if no tool needed)               │
│ 3. System executes each tool                                                │
│ 4. Tool results added to conversation as tool-role messages                 │
│ 5. Continue to model for final response                                     │
│ 6. Repeat from step 2 if model calls more tools                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

A single user turn may result in multiple tool call rounds. This is called multi-step tool use or ReAct-style reasoning.

## Parallel Tool Calls

Many models can produce multiple tool calls in a single response, to be executed in parallel:

```json
{
  "tool_calls": [
    {
      "id": "call_1",
      "function": {"name": "get_service_metrics", "arguments": "{...}"}
    },
    {
      "id": "call_2",
      "function": {"name": "get_service_metrics", "arguments": "{...}"}
    }
  ]
}
```

Parallel calls reduce round trips when independent information is needed. The calling system must match each result back to the tool call ID when returning results.

## Tool Choice Control

Request parameters can control how aggressively the model uses tools:

| tool_choice value | Behavior |
|---|---|
| `"auto"` | Model decides whether to use tools |
| `"required"` | Model must call at least one tool |
| `"none"` | Model cannot call tools even if defined |
| `{"type": "function", "function": {"name": "..."}}` | Force a specific tool call |

## Why Tool Calling Is A Platform Concern

Tool calling is not only a model feature. It creates a platform surface:

### Authorization

Not every agent or request should be allowed to call every tool. Platform layers need to validate tool invocations against the identity and scope of the caller.

```
Agent A  → can call: query_rag, get_metrics
Agent B  → can call: query_rag, get_metrics, create_deployment
```

### Sandboxing

Tools that execute code, write data, or call external services need isolation. Uncontrolled tool access is a direct path to injection and privilege escalation.

### Auditability

Every tool call should be logged with:
- the tool name and arguments
- the calling agent or session identity
- the tool result
- the model's decision to call it (the assistant turn before execution)

### Latency

Each tool call adds a round trip. Multi-step tool use can chain several round trips before the user sees a final answer. Latency budgets must account for this.

### Failure Handling

Tools fail. The model needs to receive a structured error result so it can reason about what went wrong rather than getting stuck waiting.

```json
{
  "role": "tool",
  "tool_call_id": "call_1",
  "content": "{\"error\": \"service not found\", \"service_name\": \"nonexistent-svc\"}"
}
```

## Tool Descriptions Matter

The model decides whether and how to call a tool based on its description. Poor descriptions lead to:

- tools called with wrong arguments
- tools skipped when they should have been used
- tool choice hallucinations (model invents tool names that do not exist)

Well-written tool descriptions include:

- what the tool does
- what the parameters mean
- what edge cases or constraints apply
- example argument values (optionally embedded in the description)

## The MCP Connection

Model Context Protocol (MCP) is a standardized protocol for exposing tools and resources to models. It formalizes tool definition, discovery, and invocation in a way that works across different model backends and host systems.

Module 10 covers MCP as a platform surface in depth. The key connection here is that tool calling is the application-layer protocol and MCP is one way to govern and expose tools across a platform boundary.

## Summary

Tool calling turns language models from information retrieval systems into action-oriented systems. That shift has significant implications for platform engineering:

- every callable tool is an attack surface
- every tool invocation is an auditable event
- multi-step tool use multiplies latency per user turn
- tool schemas are contracts that need versioning and governance
- the platform controls what tools exist, which agents can use them, and what happens when they fail
