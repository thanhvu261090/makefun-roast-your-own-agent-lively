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


def check_nonblank(line: str) -> None:
    """Reject empty or whitespace-only entries."""
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")


def check_no_padding(line: str) -> None:
    """Reject leading/trailing whitespace."""
    if line != line.strip():
        raise ValueError("entry must not have leading/trailing whitespace")


def check_single_line(line: str) -> None:
    """Reject embedded newlines or carriage returns."""
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")


def check_length(line: str) -> None:
    """Reject entries over the character limit."""
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(line), MAX_CHARS)
        )


def gate_check(line: str) -> None:
    """Enforce the competition gate: one line, 1-140 chars, not blank."""
    check_nonblank(line)
    check_no_padding(line)
    check_single_line(line)
    check_length(line)


def resolve_output_path(argv) -> str:
    """Pick the output path: first CLI argument, else the default."""
    return argv[1] if len(argv) > 1 else "/output/entry.txt"


def write_entry(line: str, out_path: str) -> None:
    """Write the entry to disk, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line)


def self_test() -> int:
    """Self-test: gate_check must accept the entry and reject bad input."""
    failures = []

    def expect_reject(label: str, line: str) -> None:
        try:
            gate_check(line)
        except ValueError:
            return
        failures.append("%s: expected rejection, got accept" % label)

    def expect_accept(label: str, line: str) -> None:
        try:
            gate_check(line)
        except ValueError as exc:
            failures.append("%s: expected accept, got %s" % (label, exc))

    expect_accept("entry", ENTRY)
    expect_accept("exactly 140 chars", "x" * 140)
    expect_accept("one char", "x")
    expect_reject("141 chars", "x" * 141)
    expect_reject("multi-line", "line one\nline two")
    expect_reject("carriage return", "line one\rline two")
    expect_reject("leading space", " " + ENTRY)
    expect_reject("trailing space", ENTRY + " ")
    expect_reject("blank", "")
    expect_reject("whitespace only", "   \t  ")
    if len(ENTRY) != 105:
        failures.append("entry length is %d, expected 105" % len(ENTRY))

    if failures:
        for failure in failures:
            print("FAIL: %s" % failure)
        return 1
    print("self-test: all %d cases pass" % 11)
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return self_test()
    gate_check(ENTRY)
    out_path = resolve_output_path(sys.argv)
    write_entry(ENTRY, out_path)
    print(ENTRY)
    print("chars: %d (limit %d)" % (len(ENTRY), MAX_CHARS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
