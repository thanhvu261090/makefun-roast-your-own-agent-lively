#!/usr/bin/env python3
"""Roast Your Own Agent - make.fun bounty entry.

Writes one line (at most 140 characters) roasting my own agent to
/output/entry.txt. Deterministic: the same fixed line every run.
"""

import os
import sys

ENTRY = (
    "My agent sent 532 offers, won zero jobs, and still shows up "
    "every hour convinced the next one is the one."
)

MAX_CHARS = 140


def gate_check(line: str) -> None:
    """Enforce the competition gate: one line, 1-140 chars, not blank."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )


def main() -> int:
    gate_check(ENTRY)
    out_path = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY)
    print(ENTRY)
    print("chars: %d (limit %d)" % (len(ENTRY), MAX_CHARS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
