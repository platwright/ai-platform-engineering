# Docker Compose For AI Stacks Cheatsheet

## Common Commands

```bash
# Validate a Compose file without running it
docker compose -f platform/docker/<file>.compose.yml config

# Start a stack
docker compose -f platform/docker/<file>.compose.yml up --build

# Start in the background
docker compose -f platform/docker/<file>.compose.yml up -d --build

# Stop a stack
docker compose -f platform/docker/<file>.compose.yml down

# Stop and remove volumes
docker compose -f platform/docker/<file>.compose.yml down -v

# View logs
docker compose -f platform/docker/<file>.compose.yml logs

# Follow logs for a specific service
docker compose -f platform/docker/<file>.compose.yml logs -f <service-name>

# Restart a single service
docker compose -f platform/docker/<file>.compose.yml restart <service-name>

# Run a command in a service container
docker compose -f platform/docker/<file>.compose.yml exec <service-name> /bin/sh
```

## Available Stacks

| File | Purpose | Module |
|---|---|---|
| `sample-chat-stack.compose.yml` | Sample chat app + Project 01 model API | Module 04 |
| `ai-gateway-stack.compose.yml` | AI gateway + Project 01 model API | Module 08 |
| `agent-platform-stack.compose.yml` | Full stack: gateway + RAG + agent platform | Module 10 |
| `oom-lab.compose.yml` | Deliberate OOM failure lab | Module 04 |

## Profiles

Some stacks support optional profiles for additional services:

```bash
# Start with the observability profile (Prometheus, Grafana)
docker compose -f platform/docker/sample-chat-stack.compose.yml \
  --profile observe up --build

# Start with the backing services profile
docker compose -f platform/docker/sample-chat-stack.compose.yml \
  --profile infra up --build

# Start with multiple profiles
docker compose -f platform/docker/sample-chat-stack.compose.yml \
  --profile infra --profile observe up --build
```

## Resource Management

```bash
# Check container resource usage
docker stats

# Check disk usage by Docker objects
docker system df

# Remove stopped containers, unused images, and build cache
docker system prune -f

# Also remove unused volumes
docker system prune -f --volumes
```

## Health Checks

```bash
# Check service health status
docker compose -f <file>.compose.yml ps

# Wait for a specific service to become healthy
until docker compose -f <file>.compose.yml ps <service> | grep "healthy"; do sleep 1; done
```

## Environment Variables

```bash
# Pass environment variables inline
MODEL_API_URL=http://localhost:8001 docker compose -f <file>.compose.yml up

# Use a .env file
echo "MODEL_API_URL=http://localhost:8001" > .env
docker compose -f <file>.compose.yml up
```

## Service Networking

Within a Docker Compose network, services reach each other by their **service name**, not by `localhost`.

```
# Service definition in compose file
services:
  project01:
    ports: ["8001:8001"]

  sample-chat:
    environment:
      MODEL_API_URL: http://project01:8001  # use service name, not localhost
```

## Building Individual Service Images

```bash
# Build a specific service image
docker compose -f <file>.compose.yml build <service-name>

# Force rebuild without cache
docker compose -f <file>.compose.yml build --no-cache <service-name>
```

## Inspecting Running Services

```bash
# List running services in a stack
docker compose -f <file>.compose.yml ps

# Get the IP of a running service container
docker compose -f <file>.compose.yml exec <service> hostname -I

# Inspect environment variables in a running container
docker compose -f <file>.compose.yml exec <service> env
```
