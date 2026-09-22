#!/usr/bin/env python3
"""
Check RAG index staleness across all registered services.
Exits with code 1 if any index exceeds the max age threshold.

Usage:
    python check_staleness.py                     # 24-hour default threshold
    python check_staleness.py --max-age-hours 4   # custom threshold
    python check_staleness.py --state-dir path/to/state --max-age-hours 8
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def check_staleness(state_dir: Path, max_age_hours: float) -> list[dict]:
    violations: list[dict] = []

    index_files = sorted(state_dir.glob("*.json"))
    if not index_files:
        print(f"No index files found in {state_dir}")
        return violations

    for path in index_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[ERROR] Could not read {path.name}: {exc}")
            continue

        for tenant, tdata in data.get("tenants", {}).items():
            updated_at = tdata.get("updated_at")
            chunk_count = len(tdata.get("chunks", []))

            if not updated_at:
                print(f"[WARN]  {path.stem} / {tenant}: missing updated_at field")
                violations.append({
                    "service": path.stem,
                    "tenant": tenant,
                    "age_hours": None,
                    "chunk_count": chunk_count,
                    "issue": "missing updated_at",
                })
                continue

            updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            age_hours = (datetime.now(timezone.utc) - updated_dt).total_seconds() / 3600
            status = "STALE" if age_hours > max_age_hours else "OK"

            print(
                f"[{status:<5}] {path.stem} / {tenant}: "
                f"{age_hours:.1f}h old, {chunk_count} chunks"
            )

            if age_hours > max_age_hours:
                violations.append({
                    "service": path.stem,
                    "tenant": tenant,
                    "age_hours": round(age_hours, 1),
                    "chunk_count": chunk_count,
                })

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check RAG index freshness. Exits 1 if any index is stale."
    )
    parser.add_argument(
        "--state-dir",
        default="projects/project-03-rag-platform/state",
        help="Directory containing the RAG index JSON files.",
    )
    parser.add_argument(
        "--max-age-hours",
        type=float,
        default=24.0,
        help="Maximum acceptable index age in hours (default: 24).",
    )
    args = parser.parse_args()

    state_dir = Path(args.state_dir)
    if not state_dir.is_dir():
        print(f"State directory not found: {state_dir}")
        return 1

    print(f"Checking index freshness in {state_dir} (threshold: {args.max_age_hours}h)\n")
    violations = check_staleness(state_dir, args.max_age_hours)

    print()
    if violations:
        print(f"{len(violations)} stale index(es) found. Re-ingest to restore freshness.")
        return 1

    print("All indexes are within the freshness threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
