#!/usr/bin/env python3
"""Run a small Twister smoke suite and summarize results.

This helper wraps a common command shape for quick local validation.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Twister smoke test")
    parser.add_argument(
        "--platform",
        action="append",
        default=["native_sim"],
        help="Twister platform to test (can be repeated)",
    )
    parser.add_argument(
        "--testsuite-root",
        default="tests",
        help="Path passed to twister -T (default: tests)",
    )
    parser.add_argument(
        "--outdir",
        default="twister-out-smoke",
        help="Twister output directory",
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="Extra argument forwarded to twister",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if shutil.which("twister") is None:
        print("error: 'twister' not found in PATH")
        return 2

    cmd = ["twister", "-T", args.testsuite_root, "--outdir", args.outdir]
    for platform in args.platform:
        cmd.extend(["-p", platform])
    cmd.extend(args.extra_arg)

    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, check=False)

    report = Path(args.outdir) / "twister.json"
    if report.exists():
        try:
            data = json.loads(report.read_text(encoding="utf-8"))
            testsuites = data.get("testsuites", [])
            statuses: dict[str, int] = {}
            for suite in testsuites:
                status = suite.get("status", "unknown")
                statuses[status] = statuses.get(status, 0) + 1

            print("\nTwister summary:")
            for key in sorted(statuses):
                print(f"  {key}: {statuses[key]}")
            print(f"  total: {len(testsuites)}")
        except json.JSONDecodeError:
            print("warning: could not parse twister.json")

    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
