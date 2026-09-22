# Module 10 - Agent Platform

## Overview

This module focuses on safe, operable agent capabilities rather than agent hype. It explains what an agent actually is in platform terms: a model combined with tools, state, control logic, policy, and auditability.

The module uses Project 04 as its executable companion and grounds the discussion in platform-facing tasks such as querying RAG services and gateway metrics while requiring approval for destructive actions.

## Learning Objectives

By the end of this module, you should be able to:

- explain the architecture of an agent in operational terms
- distinguish workflows, agents, and multi-agent systems
- reason about tool execution as a platform surface
- describe how state and memory affect agent behavior
- explain MCP concepts in terms relevant to platform engineering
- identify gateway, sandboxing, and approval concerns for agent systems
- run a local agent platform that safely queries other platform services

## Prerequisites

- Completion of [modules/09-rag-platform/README.md](../09-rag-platform/README.md)
- Familiarity with the gateway and RAG platform slices from earlier modules

## Difficulty And Time

- Difficulty: Intermediate to advanced
- Estimated time: 6 to 8 hours

## Module Map

### Chapters

1. [AI Agents](chapters/01-ai-agents.md)
2. [Agent Workflows](chapters/02-agent-workflows.md)
3. [Tool Execution](chapters/03-tool-execution.md)
4. [Agent State and Memory](chapters/04-agent-state-and-memory.md)
5. [Model Context Protocol](chapters/05-model-context-protocol.md)
6. [Hosting MCP Servers](chapters/06-hosting-mcp-servers.md)
7. [MCP Gateway](chapters/07-mcp-gateway.md)
8. [Agent Sandboxing](chapters/08-agent-sandboxing.md)
9. [Human-in-the-Loop Operations](chapters/09-human-in-the-loop-operations.md)

### Module Assets

- [Concepts](concepts.md)
- [Architecture](architecture.md)
- [Hands-On Lab](lab.md)
- [Challenge](challenge.md)
- [Verification](verification.md)
- [Solution](solution.md)
- [References](references.md)

### Associated Assets

- [projects/project-04-agent-platform/README.md](../../projects/project-04-agent-platform/README.md)
- [applications/sample-agent/README.md](../../applications/sample-agent/README.md)
- [projects/project-03-rag-platform/README.md](../../projects/project-03-rag-platform/README.md)
- [platform/docker/agent-platform-stack.compose.yml](../../platform/docker/agent-platform-stack.compose.yml)

## Expected Outcome

At the end of this module, you should have:

- a clear explanation of agent architecture grounded in platform concerns
- a working local agent platform that can call safe tools against other services
- a concrete example of human approval protecting a destructive action
- notes on how tool discovery, policy, and audit should evolve in later modules

## Knowledge Check

1. What makes an agent different from a simple workflow?
2. Why is tool execution a platform concern instead of only an application detail?
3. What kinds of state should agents keep, and where should that state live?
4. Why do discovery and authorization matter for MCP-style tool systems?
5. Why are sandboxing and approval critical for agent safety?
6. What should an agent run artifact capture for debugging and audit?

## Common Mistakes

- calling any tool loop an agent without defining control or policy
- letting agents invoke destructive tools without approval or audit
- hiding tool behavior so operators cannot see what happened
- treating agent memory as an undefined blob instead of a designed state model
- discussing MCP only as a protocol detail rather than as a platform surface

## Production Considerations

- tool discovery and access policy are as important as model quality
- destructive actions should require explicit approval or scoped credentials
- agent state needs retention, privacy, and debugging rules
- agent observability must capture tool calls, approvals, and failures across the loop

## Next Step

Read [concepts.md](concepts.md), then work through [projects/project-04-agent-platform/README.md](../../projects/project-04-agent-platform/README.md) using [lab.md](lab.md).