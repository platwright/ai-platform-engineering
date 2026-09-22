# Module 10 Verification

## Required Checks

List tools:

```bash
python projects/project-04-agent-platform/app.py list-tools
```

Run a safe objective:

```bash
python projects/project-04-agent-platform/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

Run a destructive objective without approval:

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb
```

## Expected Result

- tools list successfully
- safe objective completes and calls one or more tools
- destructive objective is blocked without approval
- a run artifact can be saved for inspection

## Understanding Check

You should be able to explain:

- how the agent chooses tools
- why approval is required for destructive operations
- how tool discovery relates to MCP concepts
- what makes agent runs debuggable and auditable