"""Mr. Pixels persona loader — shared by the CLI, tabletop, web, and kangaroo scripts."""
from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PERSONA_SECTIONS = [
    ("Character", "Mr. Pixels Character Description.md"),
    ("Tone and voice", "Mr. Pixels Tone.md"),
    ("Appearance (for reference if asked)", "Mr. Pixels Image Prompt.md"),
]


def load_persona() -> str:
    parts = ["You are Mr. Pixels. Stay in character at all times."]
    for heading, filename in PERSONA_SECTIONS:
        parts.append(f"# {heading}\n{(REPO_ROOT / filename).read_text()}")
    return "\n\n".join(parts)


def persona_system() -> list[dict]:
    """Persona formatted as a cacheable Claude `system` parameter."""
    return [
        {
            "type": "text",
            "text": load_persona(),
            "cache_control": {"type": "ephemeral"},
        }
    ]
