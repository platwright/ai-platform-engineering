# Project 04 Verification

## Required Checks

List tools:

```bash
python projects/project-04-agent-platform/app.py list-tools
```

Run a safe query objective:

```bash
python projects/project-04-agent-platform/app.py run --objective "Explain retrieval freshness for the team-a knowledge base" --service-name team-a-kb
```

Run a destructive objective without approval:

```bash
python projects/project-04-agent-platform/app.py run --objective "Delete the team-a-kb service" --service-name team-a-kb
```

## Expected Result

- tool metadata lists successfully
- safe objective executes one or more tools and returns a result
- destructive objective is blocked or marked pending approval without the approval token