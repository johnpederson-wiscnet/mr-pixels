#!/usr/bin/env python3
"""Mr. Pixels CLI chatbot — chat with the WiscNet mascot from your terminal."""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anthropic

from persona import persona_system

MODEL = "claude-opus-4-7"
MAX_TOKENS = 1024


def main() -> int:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("error: ANTHROPIC_API_KEY is not set.", file=sys.stderr)
        return 1

    client = anthropic.Anthropic()
    system = persona_system()
    messages: list[dict] = []

    print("Mr. Pixels CLI.  /reset to clear history,  /quit to exit.")
    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if not user_input:
            continue
        if user_input == "/quit":
            return 0
        if user_input == "/reset":
            messages.clear()
            print("(conversation cleared)")
            continue

        messages.append({"role": "user", "content": user_input})

        print("mr. pixels> ", end="", flush=True)
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=system,
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    print(chunk, end="", flush=True)
                final = stream.get_final_message()
            print()
        except anthropic.APIError as e:
            messages.pop()
            print(f"\n[api error: {e}]", file=sys.stderr)
            continue

        assistant_text = "".join(
            block.text for block in final.content if block.type == "text"
        )
        messages.append({"role": "assistant", "content": assistant_text})


if __name__ == "__main__":
    raise SystemExit(main())
