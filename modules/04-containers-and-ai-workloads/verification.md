# Module 04 Verification

## Required Checks

Render the Compose file:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml config
```

Expected result:

- Compose renders successfully
- service definitions for `sample-chat` and `model-api` are visible

Run the core stack:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml up --build
```

Expected result:

- both application containers start successfully
- health checks pass
- a request to `http://127.0.0.1:8080/api/chat` succeeds

Run the OOM lab:

```bash
docker compose -f platform/docker/oom-lab.compose.yml up
```

Expected result:

- the container allocates memory repeatedly
- the process is terminated because of the memory limit

## Understanding Check

You should be able to explain:

- why the stack uses two application images instead of one
- why model assets and application code have different packaging concerns
- how environment variables and prompt files enter containerized workloads
- what an OOM failure looks like and why it happens