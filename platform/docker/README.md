# Docker Assets

This area holds container and Docker Compose assets used in Module 04.

## Available Assets

- [sample-chat-stack.compose.yml](sample-chat-stack.compose.yml): local stack for the sample chat application and Project 01 model API
- [oom-lab.compose.yml](oom-lab.compose.yml): deliberate container OOM lab for resource-management practice
- [labs/oom_memory_hog.py](labs/oom_memory_hog.py): helper script used by the OOM lab
- [ai-gateway-stack.compose.yml](ai-gateway-stack.compose.yml): local stack for the AI gateway and Project 01 model API
- [agent-platform-stack.compose.yml](agent-platform-stack.compose.yml): local stack for the gateway, RAG platform, and agent platform capabilities

## Related Images

- [applications/sample-chat/Dockerfile](../../applications/sample-chat/Dockerfile)
- [projects/project-01-model-api/Dockerfile](../../projects/project-01-model-api/Dockerfile)

## Typical Commands

Render the Compose configuration:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml config
```

Run the application and model API:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml up --build
```

Run the extended local stack with backing services:

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml --profile infra --profile observe up --build
```

Run the AI gateway stack:

```bash
docker compose -f platform/docker/ai-gateway-stack.compose.yml up --build
```

Run the agent platform stack:

```bash
docker compose -f platform/docker/agent-platform-stack.compose.yml up --build
```