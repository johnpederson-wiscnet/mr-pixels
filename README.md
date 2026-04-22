# Mr. Pixels

Character bible and chatbot for Mr. Pixels — WiscNet's cigar-chewing, story-spinning
chimpanzee mascot.

## Contents

- `Mr. Pixels Character Description.md` — who he is
- `Mr. Pixels Tone.md` — how he talks
- `Mr. Pixels Image Prompt.md` — what he looks like
- `chat/` — CLI chatbot that loads the three persona files as a Claude system prompt

## CLI chatbot

Talk to Mr. Pixels from your terminal. Uses the Anthropic Python SDK with Claude Opus 4.7
and prompt caching on the persona.

### Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r chat/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

### Run

```sh
python chat/chat.py
```

Commands inside the chat:

- `/reset` — clear conversation history
- `/quit` — exit (Ctrl-C also works)
