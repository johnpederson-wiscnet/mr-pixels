# Mr. Pixels

Character bible and automation for Mr. Pixels — WiscNet's cigar-chewing,
story-spinning chimpanzee mascot.

## Contents

- `Mr. Pixels Character Description.md` — who he is
- `Mr. Pixels Tone.md` — how he talks
- `Mr. Pixels Image Prompt.md` — what he looks like
- `chat/` — Claude-powered scripts that use the three persona files as a shared
  system prompt
- `.github/workflows/kangaroo.yml` — daily kangaroo-boxing fact on a schedule

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r chat/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

All scripts load the same persona via `chat/persona.py` and use Claude Opus 4.7
with prompt caching on the persona prefix.

## CLI chatbot

```sh
python chat/chat.py
```

Commands inside the chat: `/reset` clears history, `/quit` exits.

## Tabletop cybersecurity exercise generator

Generate a Mr. Pixels-hosted tabletop exercise from a one-line scenario:

```sh
python chat/tabletop.py "ransomware attack on a county WAN"
```

Output is Markdown with scenario, injects, discussion rounds, and wrap-up.

## Web UI

```sh
uvicorn chat.web:app --reload
```

Then open <http://127.0.0.1:8000>. Same persona, streams responses in the
browser.

## Daily kangaroo fact

`python chat/kangaroo.py` generates today's kangaroo-boxing fact (canon:
Mr. Pixels starts every day with one) and appends it to `KANGAROO_LOG.md`.
Idempotent — rerunning on the same day is a no-op.

The GitHub Action in `.github/workflows/kangaroo.yml` runs this daily at
13:00 UTC and commits the result. Requires a repo secret named
`ANTHROPIC_API_KEY`.
