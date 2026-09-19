# Chapter 0.4 - Repository Workflow

## Why Your Fork Matters

Your fork is not only a copy of the course. It is your workbook.

You should expect to add:

- progress notes
- architecture sketches
- challenge answers
- your own lab solutions
- follow-up experiments

## Recommended Personal Directories

The repository provides a small initialization script that creates:

- `progress/`
- `my-notes/`
- `my-solutions/`

Use them consistently.

## Suggested Working Pattern

1. Pull the latest upstream changes.
2. Sync your fork.
3. Work through a module.
4. Write what you learned in your workbook.
5. Save your own commands, diagrams, and troubleshooting notes.
6. Repeat.

## Why This Workflow Is Useful

AI platform engineering is operational knowledge. You will retain more if you create your own notes, commands, and decisions rather than passively reading.

## Reference Setup Commands

PowerShell:

```powershell
./scripts/setup/init-workbook.ps1
```

Bash:

```bash
./scripts/setup/init-workbook.sh
```

## Suggested Branching Approach

Keep your main branch close to upstream and use short-lived branches when you want to experiment with labs or extra notes that may later become contribution candidates.

## Contribution Mindset

If you find a broken instruction, unclear concept, or better verification step, capture it in your notes first, then consider contributing the improvement back upstream later.