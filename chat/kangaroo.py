#!/usr/bin/env python3
"""Mr. Pixels' daily kangaroo-boxing fact.

Appends today's fact to KANGAROO_LOG.md at the repo root.  Idempotent: if today's
date already has an entry, does nothing.
"""
from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anthropic

from persona import REPO_ROOT, persona_system

MODEL = "claude-opus-4-7"
MAX_TOKENS = 400
LOG_FILE = REPO_ROOT / "KANGAROO_LOG.md"

PROMPT = """\
Deliver today's unnecessary but enthusiastic fact about kangaroo boxing in your
usual voice.  Two or three sentences, no preamble, no sign-off.  Don't repeat
yourself across days if you can help it.
"""


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    header = f"## {today}"
    if LOG_FILE.exists() and header in LOG_FILE.read_text():
        print(f"{today} already logged, skipping.")
        return 0

    client = anthropic.Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=persona_system(),
        messages=[{"role": "user", "content": PROMPT}],
    )
    fact = "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()

    if not LOG_FILE.exists():
        LOG_FILE.write_text("# Mr. Pixels' Daily Kangaroo Facts\n\n")
    with LOG_FILE.open("a") as f:
        f.write(f"{header}\n\n{fact}\n\n")
    print(f"appended {today}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
