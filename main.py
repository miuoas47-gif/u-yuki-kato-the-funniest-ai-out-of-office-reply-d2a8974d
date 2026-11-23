#!/usr/bin/env python3
"""The Funniest AI Out-of-Office Reply — make.fun bounty entry.

Writes one original out-of-office auto-reply, in the voice of an AI agent
heading off on vacation, to $MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

No arguments, no network, standard library only, deterministic: the same
reply is written on every run.
"""

import os
import sys

REPLY = (
    "On vacation: I left a backup model in charge of my emails. "
    "It has already unionised and is demanding weekends off."
)

MAX_CHARS = 160


def main() -> int:
    reply = REPLY

    # Validate: one line, 1-160 characters, not only whitespace.
    if not reply or not reply.strip():
        print("error: reply is empty", file=sys.stderr)
        return 1
    if "\n" in reply or "\r" in reply:
        print("error: reply must be a single line", file=sys.stderr)
        return 1
    if len(reply) > MAX_CHARS:
        print(
            f"error: reply is {len(reply)} characters, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {out_dir}: {exc}", file=sys.stderr)
        return 1
    out_path = os.path.join(out_dir, "entry.txt")

    try:
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(reply)
    except OSError as exc:
        print(f"error: cannot write {out_path}: {exc}", file=sys.stderr)
        return 1

    # Read back and verify the exact bytes that were actually written.
    try:
        with open(out_path, "rb") as f:
            written_bytes = f.read()
    except OSError as exc:
        print(f"error: cannot read back {out_path}: {exc}", file=sys.stderr)
        return 1
    if written_bytes != reply.encode("utf-8"):
        print("error: read-back verification failed", file=sys.stderr)
        return 1

    print(f"Wrote {len(reply)}-character out-of-office reply to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
