# Prerequisites

## Baseline Skills

You should ideally be comfortable with:

- Git
- Linux basics
- Networking basics
- Docker basics
- REST APIs
- Basic Python
- Basic cloud concepts

Basic Kubernetes knowledge is useful but not mandatory.

## Required Tooling

The course is local-first. Most foundational labs assume the following tools are available:

| Tool | Why it matters |
| --- | --- |
| Git | clone, branch, and track your work |
| Python 3.11+ | small utilities, scripts, and AI application examples |
| uv or pip | Python package management |
| Docker | local container builds and stacks |
| kubectl | Kubernetes interaction |
| kind or k3d | local Kubernetes cluster |
| Helm | packaging and deploying platform components |
| Terraform or OpenTofu | infrastructure as code for later modules |
| Make | repeatable developer workflows |
| curl | API testing |
| jq | JSON inspection and automation |

## Optional Tooling

These are recommended but not required for Module 00:

- Ollama
- VS Code
- GitHub CLI

## Recommended Machine Profile

Module 00 works on modest developer laptops, but later modules become easier with:

- 16 GB RAM minimum
- 4 CPU cores minimum
- 20+ GB free disk space
- Docker Desktop or a working Docker Engine installation

GPU hardware is optional for the early course. Later modules can use hosted providers or CPU-friendly local examples where possible.

## Validation Scripts

Use one of the following scripts to check your environment:

PowerShell:

```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:

```bash
./scripts/setup/check-prereqs.sh
```

Both scripts verify the required toolchain and return a non-zero exit code when mandatory tools are missing.

## Setup Order

If you are building your environment from scratch, use this order:

1. Install Git.
2. Install Python.
3. Install Docker.
4. Install kubectl.
5. Install kind or k3d.
6. Install Helm.
7. Install Terraform or OpenTofu.
8. Install curl, jq, and Make if your system does not already provide them.
9. Run the validation script.
10. Initialize your workbook.

## If Something Fails

Start with the Module 00 troubleshooting sections:

- [modules/00-getting-started/verification.md](../modules/00-getting-started/verification.md)
- [modules/00-getting-started/solution.md](../modules/00-getting-started/solution.md)