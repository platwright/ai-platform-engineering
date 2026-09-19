# Chapter 0.3 - Local Development Environment

## Why Local First

The course begins with local tooling because it keeps the feedback loop fast and cheap. You should understand system behavior before paying for cloud infrastructure or relying on managed services.

## Required Tools

Install these before early labs:

- Git
- Python
- uv or pip
- Docker
- kubectl
- kind or k3d
- Helm
- Terraform or OpenTofu
- Make
- curl
- jq

## Optional Tools

Useful later, but not required for Module 00:

- Ollama
- VS Code
- GitHub CLI

## Recommended Install Order

1. Git
2. Python
3. Docker
4. kubectl
5. kind or k3d
6. Helm
7. Terraform or OpenTofu
8. curl, jq, and Make if your OS does not already provide them

## Verify With The Repository Script

PowerShell:

```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:

```bash
./scripts/setup/check-prereqs.sh
```

The script is intentionally simple. Its job is to catch missing tools early rather than diagnose every local issue.

## Practical Notes

- Docker must actually run, not just be installed.
- Python should be modern enough for current packaging and AI examples.
- A local Kubernetes cluster is needed later, but you do not need to create it yet.
- GPU hardware is optional for the early path.

## If You Are Missing Tools

Install the missing tool, rerun the script, and note the issue in your workbook. That habit matters later when the failures are platform failures instead of workstation failures.