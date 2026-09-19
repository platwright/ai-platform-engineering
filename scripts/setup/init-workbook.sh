#!/usr/bin/env bash

set -euo pipefail

destination="${1:-.}"
root="$(cd "${destination}" && pwd)"

mkdir -p "${root}/progress" "${root}/my-notes" "${root}/my-solutions"

create_if_missing() {
  local file_path="$1"
  local content="$2"

  if [[ -f "${file_path}" ]]; then
    echo "[SKIPPED] ${file_path} already exists"
    return 0
  fi

  printf "%s" "${content}" > "${file_path}"
  echo "[CREATED] ${file_path}"
}

create_if_missing "${root}/progress/README.md" $'# Progress\n\nTrack module-by-module progress here.\n'
create_if_missing "${root}/progress/module-00.md" $'# Module 00 Progress\n\n## Starting point\n\n- Current role:\n- Familiar areas:\n- New areas:\n- Why this course:\n'
create_if_missing "${root}/my-notes/README.md" $'# My Notes\n\nStore your personal notes, diagrams, and reflections here.\n'
create_if_missing "${root}/my-solutions/README.md" $'# My Solutions\n\nStore your challenge answers and lab solutions here.\n'

echo
echo "Workbook initialization complete."