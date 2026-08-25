#!/bin/bash
set -euo pipefail

# Only run in Claude Code on the web (remote) sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# This repo is a markdown (Obsidian) vault with no app dependencies.
# Install the markdown linter so lint checks work in web sessions.
if ! command -v markdownlint-cli2 >/dev/null 2>&1; then
  npm install -g markdownlint-cli2
fi

echo "Session setup complete: markdownlint-cli2 $(markdownlint-cli2 --help 2>/dev/null | head -1 || true)"
