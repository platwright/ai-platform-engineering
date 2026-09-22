# Troubleshooting

## Environment Setup

### Prerequisite Script Reports Missing Tools

Install the missing tool and rerun the check.

PowerShell:
```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:
```bash
./scripts/setup/check-prereqs.sh
```

If the script says a tool is missing but it is installed, check whether it is on your `PATH`. For example, Python installations on Windows may install as `python3` rather than `python`, or `py` from the Windows Python launcher.

### Python Version Errors

The course requires Python 3.11 or later. Check your version:

```bash
python --version
# or
python3 --version
```

If you have multiple Python versions, use `uv` or a virtual environment to isolate the course dependencies.

### Docker Is Installed But Not Running

Start Docker Desktop or your local Docker Engine before retrying labs that depend on container workflows.

On Linux:
```bash
sudo systemctl start docker
docker info  # should succeed
```

On macOS and Windows, ensure Docker Desktop is running (check the system tray icon).

### kubectl Exists But No Cluster Is Running

That is expected for Module 00. Later modules will require a local Kubernetes cluster.

For Module 05 and later, start a local cluster:
```bash
# kind
kind create cluster --name ai-platform

# k3d
k3d cluster create ai-platform
```

Verify with:
```bash
kubectl cluster-info
kubectl get nodes
```

### Workbook Script Already Finds Existing Files

That is expected. The script is idempotent and skips files that already exist. Re-running it is safe.

### Windows Users And Make

If `make` is missing on Windows, you can work through early conceptual material without it. For later automation-heavy modules, install either:

- [GNU Make for Windows](https://gnuwin32.sourceforge.net/packages/make.htm)
- or use PowerShell equivalents for any `make` targets

---

## Python Applications

### ModuleNotFoundError When Running Project Code

The project code uses only the Python standard library by default. If you see an import error, check that you are running the correct Python version and from the repository root.

If you have installed optional dependencies, confirm they are installed in the active virtual environment:
```bash
pip list | grep <package-name>
```

### Config File Not Found

Most projects read from a `config/app.json` file. Copy the example before running:
```bash
cp projects/project-01-model-api/config/app.example.json projects/project-01-model-api/config/app.json
```

Repeat for any other project you are working with.

### Connection Refused When Calling Project 01

Project 01 needs to be running before other services or applications try to call it. In a separate terminal:
```bash
python projects/project-01-model-api/app.py serve
```

Wait for the message indicating the server is listening before calling it from other processes.

### JSON Decode Errors In Run Artifacts

If a run artifact contains malformed JSON, it usually means the provider returned an error response that was written as-is. Check the response field in the artifact for an error message from the provider.

---

## Docker and Compose

### Build Fails With No Space Left On Device

Docker build layers and model weights consume significant disk space. Free up space with:
```bash
docker system prune -f
docker volume prune -f
```

Be careful: `prune` removes stopped containers and unused images. Confirm you do not need them before running.

### Port Already In Use

If a Compose service fails to start because a port is occupied, find what is using it:

```bash
# Linux and macOS
lsof -i :8080

# Windows PowerShell
netstat -ano | findstr :8080
```

Either stop the conflicting process or change the host port mapping in the Compose file.

### Compose Container Exits Immediately

Check the container logs:
```bash
docker compose -f <file> logs <service-name>
```

Common causes:
- missing environment variable that the container requires
- failed health check because a dependency was not ready
- application startup error (check Python traceback in the logs)

### Services Cannot Reach Each Other In Compose

Within a Docker Compose network, services reach each other by their service name, not by `localhost`. If an application is configured to call `http://localhost:8001`, it will not reach a sibling service. Use the service name instead: `http://project01:8001`.

---

## Kubernetes

### Pods Stuck In Pending State

Usually caused by insufficient resources or a scheduling constraint that cannot be satisfied.

Check events:
```bash
kubectl describe pod <pod-name> -n <namespace>
```

Common causes:
- `Insufficient cpu` or `Insufficient memory`: reduce resource requests or add more nodes
- `no nodes available to schedule pods`: your local cluster may be out of capacity
- `node(s) had taint that the pod didn't tolerate`: the pod needs a toleration for a GPU or special node taint

### ImagePullBackOff

The container image cannot be pulled. Check:
1. Is the image name and tag correct?
2. For custom images, did the build succeed and is the image available locally?
3. For `kind` clusters, load local images with `kind load docker-image <image>` before applying the manifest.

### kubectl Kustomize Command Fails

Ensure you have `kubectl` version 1.21 or later, which includes the kustomize subcommand. You can also install `kustomize` separately and run:
```bash
kustomize build platform/kubernetes/<directory>
```

---

## AI Gateway and Model Serving

### AI Gateway Returns 503

The gateway is healthy but cannot reach the upstream model provider. Check:
1. Is Project 01 or the model server running?
2. Is the upstream endpoint URL correct in the gateway configuration?
3. Is there a network policy or firewall blocking the gateway-to-model connection?

### Gateway Returns Correct Status But Wrong Model Output

The gateway is routing, but the model provider may have changed behavior. Check:
- gateway logs for which provider was selected
- whether the request is hitting a mock provider or a real provider
- whether the upstream provider has changed its API or model behavior

### TTFT Is Very High (> 5 Seconds)

Common causes:
- the model server is still loading the model into memory (wait and retry)
- the request prompt is very long, driving high prefill time
- the GPU memory is nearly full, causing KV cache eviction and recomputation
- the request is queuing behind other long requests

---

## RAG Platform

### Ingestion Produces Zero Chunks

Check:
1. Does the documents directory exist and contain files?
2. Are the files in a supported format (plain text by default)?
3. Is the configured chunk size small enough to produce at least one chunk from the smallest file?

### Query Returns No Results

Check:
1. Has ingestion been run for the tenant being queried?
2. Does the state directory contain an index file for that tenant?
3. Is the question phrased in a way that has any overlap with the indexed content?

### Sample RAG App Cannot Reach The Gateway

The sample-rag application calls the AI gateway for grounded generation. Ensure the gateway is running and that the gateway URL in `config/app.json` points to the correct host and port.

---

## Agent Platform

### Agent Runs But Never Calls A Tool

The mock agent uses a simple keyword-based tool selection strategy. If your objective does not contain keywords that match the configured tools, no tool will be called. Try an objective that explicitly names what you want to look up.

### Destructive Action Not Being Blocked

Check that:
1. The approval token is not set (if `--approval-token` is omitted, destructive actions should be blocked)
2. The tool classification in the tool registry correctly marks the tool as requiring approval

### Agent Run Artifact Is Empty Or Missing

Check that the `runs/` directory exists and is writable. The agent writes artifacts at the end of each run. If the run crashed mid-execution, the artifact may not have been written.

---

## General

### Repository Clone Is Slow

The repository contains large binary fixtures. If you have bandwidth constraints, use a shallow clone:
```bash
git clone --depth=1 https://github.com/<repo-url>
```

### Links In Markdown Files Are Broken

All module links use paths relative to the module directory. If you are viewing files locally outside a browser, relative links may not resolve correctly. Open the repository in VS Code or another Markdown-aware editor that resolves relative links.

### Course Content Seems Outdated

The repository is updated progressively. If you find outdated instructions, tool version conflicts, or broken steps, please open an issue or pull request following the guidance in [CONTRIBUTING.md](../CONTRIBUTING.md).
