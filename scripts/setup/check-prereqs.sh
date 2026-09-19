#!/usr/bin/env bash

set -euo pipefail

test_tool() {
  local label="$1"
  shift

  for name in "$@"; do
    if command -v "$name" >/dev/null 2>&1; then
      echo "[OK] ${label} (${name})"
      return 0
    fi
  done

  echo "[MISSING] ${label}"
  return 1
}

all_passed=true

test_tool "git" git || all_passed=false
test_tool "python" python || all_passed=false
test_tool "uv or pip" uv pip || all_passed=false
test_tool "docker" docker || all_passed=false
test_tool "kubectl" kubectl || all_passed=false
test_tool "kind or k3d" kind k3d || all_passed=false
test_tool "helm" helm || all_passed=false
test_tool "terraform or tofu" terraform tofu || all_passed=false
test_tool "make" make || all_passed=false
test_tool "curl" curl || all_passed=false
test_tool "jq" jq || all_passed=false

echo

if [[ "${all_passed}" == true ]]; then
  echo "Environment check passed."
  exit 0
fi

echo "Environment check failed. Install the missing required tools and rerun the script."
exit 1