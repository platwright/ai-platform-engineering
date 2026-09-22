# Module 04 Lab

## Goal

Containerize the sample chat stack, run it locally with Docker Compose, and trigger a deliberate OOM failure.

## Outcome

By the end of this lab, you should have:

- built the sample chat and model API images
- started the local stack with Compose
- sent a request through the full containerized path
- observed a failure lab that demonstrates memory limits in practice

## Step 1 - Review The Assets

Start with:

- [applications/sample-chat/README.md](../../applications/sample-chat/README.md)
- [projects/project-01-model-api/README.md](../../projects/project-01-model-api/README.md)
- [platform/docker/README.md](../../platform/docker/README.md)

## Step 2 - Render The Compose File

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml config
```

## Step 3 - Start The Core Stack

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml up --build
```

This runs:

- `model-api`
- `sample-chat`

## Step 4 - Send A Request

In another terminal:

```bash
curl -X POST http://127.0.0.1:8080/api/chat -H "Content-Type: application/json" -d "{\"message\":\"Explain why a model API should be separated from application logic.\"}"
```

Observe that the request moves through the sample chat application into Project 01 and returns a normalized response.

## Step 5 - Bring Up Optional Infra Services

```bash
docker compose -f platform/docker/sample-chat-stack.compose.yml --profile infra --profile observe up --build
```

This adds Redis, Qdrant, and a placeholder observability service to make the stack shape visible.

## Step 6 - Run The OOM Lab

In a separate terminal:

```bash
docker compose -f platform/docker/oom-lab.compose.yml up
```

Watch the memory hog allocate memory until the container is killed by the memory limit.

## Step 7 - Reflect

Write down:

- what belonged in the application image versus the model API image
- which settings entered via config or environment variables
- what signals helped you understand the OOM failure