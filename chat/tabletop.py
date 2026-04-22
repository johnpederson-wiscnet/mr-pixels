#!/usr/bin/env python3
"""Mr. Pixels-hosted tabletop cybersecurity exercise generator.

Usage:
    python chat/tabletop.py "ransomware attack on a county WAN"
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anthropic

from persona import persona_system

MODEL = "claude-opus-4-7"
MAX_TOKENS = 4096

TABLETOP_INSTRUCTIONS = """\
You are hosting a cybersecurity tabletop exercise for a WiscNet member organization.
Stay fully in character as Mr. Pixels.  Produce the exercise as Markdown with these
sections, in order:

## Opening monologue
A short, in-voice cold open.

## Scenario
One paragraph establishing the situation.  Keep it grounded in WiscNet-adjacent
settings (K-12 district, small municipality, rural library, community college, etc.).

## Initial injects
3 numbered events the facilitator reads at T+0.

## Discussion questions (round 1)
4 questions that test incident-identification and initial response.

## Escalating injects
3 numbered events that raise the stakes at T+30 minutes.

## Discussion questions (round 2)
4 questions that test containment, communications, and escalation.

## Wrap-up
A closing monologue with one genuinely useful takeaway buried in Mr. Pixels' usual
digressions.
"""


def main(argv: list[str]) -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1
    if len(argv) < 2:
        print(f"usage: {argv[0]} <scenario topic>", file=sys.stderr)
        return 2

    topic = " ".join(argv[1:])
    client = anthropic.Anthropic()

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=persona_system(),
        messages=[
            {
                "role": "user",
                "content": f"{TABLETOP_INSTRUCTIONS}\n\nScenario topic: {topic}",
            }
        ],
    ) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
