#!/usr/bin/env python3
"""Minimal FastAPI chat UI for Mr. Pixels.

Run:
    uvicorn chat.web:app --reload
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import anthropic
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from persona import persona_system

MODEL = "claude-opus-4-7"
MAX_TOKENS = 1024
HERE = Path(__file__).resolve().parent

app = FastAPI()
client = anthropic.Anthropic()
SYSTEM = persona_system()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (HERE / "index.html").read_text()


@app.post("/chat")
def chat(req: ChatRequest) -> StreamingResponse:
    messages = [m.model_dump() for m in req.messages]

    def generate():
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM,
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    yield chunk
        except anthropic.APIError as e:
            yield f"\n[api error: {e}]"

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")
