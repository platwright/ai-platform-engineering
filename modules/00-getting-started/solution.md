# Module 00 Solution

This file is a reference, not a script to copy without thinking.

## Expected Prerequisite Check Behavior

When your environment is ready, the setup script should report every mandatory tool as installed and exit with success.

Example summary:

```text
[OK] git
[OK] python
[OK] uv or pip
[OK] docker
[OK] kubectl
[OK] kind or k3d
[OK] helm
[OK] terraform or tofu
[OK] make
[OK] curl
[OK] jq

Environment check passed.
```

If one or more required tools are missing, the script should exit non-zero and print which capabilities are absent.

## Expected Workbook Structure

```text
progress/
  README.md
  module-00.md

my-notes/
  README.md

my-solutions/
  README.md
```

## Example Progress Note Prompts

Your `progress/module-00.md` can include:

- current role and experience level
- why you are taking the course
- current confidence with Python, Docker, Kubernetes, and AI concepts
- which modules you expect to be easiest
- which modules you expect to be hardest

## Example Role Boundary Answer

One reasonable summary:

- application teams own product behavior, prompts, and business workflows
- the AI platform team owns reusable platform capabilities, guardrails, operational tooling, and paved roads
- infrastructure teams provide the shared substrate such as Kubernetes, network, identity foundations, and compute policy

The exact line will vary by organization, but the important part is making ownership explicit.