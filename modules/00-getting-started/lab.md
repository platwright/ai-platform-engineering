# Module 00 Lab

## Goal

Validate your workstation for the early course modules and create a personal workbook structure inside your fork or local clone.

## Outcome

By the end of this lab, you should have:

- verified your required toolchain
- created workbook folders for progress, notes, and solutions
- written your first progress note for the course

## Step 1 - Fork Or Clone The Repository

If you are following the course from GitHub, fork the repository first. Your fork is your working copy and personal notebook.

Then clone your fork locally.

## Step 2 - Run The Prerequisite Check

PowerShell:

```powershell
./scripts/setup/check-prereqs.ps1
```

Bash:

```bash
./scripts/setup/check-prereqs.sh
```

If the script reports missing required tools, install them before continuing.

## Step 3 - Initialize Your Workbook

PowerShell:

```powershell
./scripts/setup/init-workbook.ps1
```

Bash:

```bash
./scripts/setup/init-workbook.sh
```

This creates:

- `progress/`
- `my-notes/`
- `my-solutions/`

## Step 4 - Capture Your Starting Point

Create or update the generated progress file with:

- your current role
- which parts of the course are already familiar
- which areas are new
- why you want to learn AI platform engineering

Suggested file:

- `progress/module-00.md`

## Step 5 - Map The Architecture In Your Own Words

In `my-notes/`, write a short note answering:

- What lives in the application layer?
- What lives in the platform layer?
- What lives in the infrastructure layer?
- Which part of that stack overlaps most with your current job?

## Step 6 - Validate Completion

Use [verification.md](verification.md) to confirm the module is complete.

## Stretch Goal

Install one optional tool you expect to use later, such as Ollama or GitHub CLI, and note why you chose it.