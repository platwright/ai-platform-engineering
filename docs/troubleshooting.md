# Troubleshooting

## Prerequisite Script Reports Missing Tools

Install the missing tool and rerun the check.

PowerShell:

```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:

```bash
./scripts/setup/check-prereqs.sh
```

## Docker Is Installed But Not Running

Start Docker Desktop or your local Docker Engine before retrying labs that depend on container workflows.

## kubectl Exists But No Cluster Is Running

That is acceptable for Module 00. Later modules will require a local Kubernetes cluster, but the getting-started module only checks tool availability.

## Workbook Script Already Finds Existing Files

That is expected. The script is idempotent and should skip files that already exist.

## Windows Users And Make

If `make` is missing on Windows, you can still work through early conceptual material. Install a compatible Make implementation before later automation-heavy modules.