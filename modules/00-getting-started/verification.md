# Module 00 Verification

Use this checklist before moving to Module 01.

## Tooling Check

Required tools should be installed and visible on your path:

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

Run one of the following and confirm the command exits successfully.

PowerShell:

```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:

```bash
./scripts/setup/check-prereqs.sh
```

## Workbook Check

Confirm these directories exist after running the workbook setup script:

- `progress/`
- `my-notes/`
- `my-solutions/`

## Understanding Check

You should be able to explain, without looking at the notes:

- the difference between AI platform engineering and ML engineering
- the difference between the application, platform, and infrastructure layers
- why the course starts local-first
- the seven-stage platform evolution used across the repository

## Reflection Check

You should have completed:

- one progress note
- one architecture note in your own words
- one short answer to the challenge prompt or an outline for it

## Exit Criteria

You are ready for Module 01 when:

- your environment check passes
- you know where your personal notes and solutions will live
- you understand the scope of the rest of the course