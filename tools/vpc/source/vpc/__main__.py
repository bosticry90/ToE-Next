"""Command-line entry point for the promoted exact verifier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import verify_paths


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="vpc",
        description="Recompute a claim-scoped finite exact DAG.",
    )
    parser.add_argument("profile", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    arguments = parser.parse_args()
    receipt = verify_paths(arguments.profile, arguments.candidate, arguments.source_root)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
