import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from . import commands
from .config import ASSISTANT_NAME, OPENAI_API_KEY

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = FastAPI(title=f"{ASSISTANT_NAME} Web")


# ── AI fallback ───────────────────────────────────────────────────────────────
# Single shared chat history for simplicity. A multi-user deployment would key
# this per-session (e.g. by a session id cookie or header) instead.

_ai_client = None
_chat_history = [
    {"role": "system", "content": (
        f"You are {ASSISTANT_NAME}, a helpful AI voice assistant. "
        "Keep responses short and conversational — two sentences max."
    )}
]

if OPENAI_API_KEY:
    try:
        from openai import OpenAI
        _ai_client = OpenAI(api_key=OPENAI_API_KEY)
    except ImportError:
        pass


def ask_ai(prompt: str) -> str:
    if not _ai_client:
        return "I'm not sure about that. Set an OPENAI_API_KEY environment variable for smarter replies."
    _chat_history.append({"role": "user", "content": prompt})
    try:
        response = _ai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=_chat_history,
            max_tokens=120,
        )
        reply = response.choices[0].message.content.strip()
        _chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"AI error: {e}"


# ── API ───────────────────────────────────────────────────────────────────────

class CommandRequest(BaseModel):
    text: str


@app.post("/api/command")
def handle_command(req: CommandRequest):
    result = commands.route(req.text)
    if result is not None:
        return result
    return {"reply": ask_ai(req.text), "action": None}


@app.get("/api/greet")
def handle_greet():
    return {"reply": commands.greet(), "action": None}


# ── static frontend ────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
