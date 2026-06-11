# 🤖 Jarvis Web

🔗 **Live demo:** [jarvisweb-ryua.onrender.com](https://jarvisweb-ryua.onrender.com)
*(free-tier instance — may take ~30-60s to wake up if it's been idle)*

A browser-based version of the **Jarvis** voice assistant. The "brain"
(command routing + OpenAI fallback) runs as a small **FastAPI** service,
while speech recognition and text-to-speech happen entirely in the browser
via the **Web Speech API** — open it from any device with a browser, no
desktop install required.

This sits alongside `jarvis-assistant/`, the original terminal/desktop
version, which is left untouched.

<img width="600" height="600" alt="image" src="https://github.com/user-attachments/assets/5df6f701-b028-41d1-9719-5f4350201ed2" />

## ✨ Features

- 🎙️ **Voice input** — talk to Jarvis with your microphone (Chrome/Edge via the Web Speech API)
- 🔊 **Spoken replies** — every response is read aloud using the browser's speech synthesis
- ⌨️ **Text chat fallback** — type commands when voice isn't available or supported
- 🌦️ **Weather lookup** — "what's the weather in Tokyo?"
- 📰 **News headlines** — top stories pulled live from BBC News
- 😂 **Jokes on demand** — random one-liners to lighten the mood
- 💬 **Motivational quotes** — random inspirational quotes
- 📖 **Wikipedia summaries** — "who is..." / "what is..." style questions
- 🔍 **Google search** — opens results in a new browser tab
- ▶️ **YouTube search** — finds and opens videos in a new tab
- 🌐 **Open any website** — "open github.com"
- 🎵 **Local music playback** — plays audio files from `static/music/`
- ⏱️ **Voice-set timers** — "set a timer for 5 minutes", with a spoken alert when done
- 🪙 **Coin flip & 🎲 dice roll** — for quick random decisions
- 🕒 **Time & date** — quick server-side clock lookups
- 🧠 **AI fallback** — anything Jarvis doesn't recognize is answered by OpenAI (optional, needs an API key)
- 🐳 **Docker-ready** — containerized for easy local runs or deployment to platforms like Render

## What changed vs. the desktop version

A server has no microphone, speakers, screen, or access to your desktop, so:

- **Removed**: opening desktop apps, screenshots, battery/CPU/RAM/IP info
  (those would describe the *server*, not your machine)
- **Moved to the browser**: speech recognition, text-to-speech, opening
  search results / websites / YouTube in a new tab, playing music, timers
- **Kept on the server**: weather, news, jokes, quotes, Wikipedia, coin
  flip / dice roll, and the OpenAI fallback for anything else

`get_time` / `get_date` report the **server's** clock — fine for a single
user, but worth noting if you deploy this for others in a different
timezone.

## Run locally

```bash
cd jarvis-web
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # then add your OPENAI_API_KEY (optional)

uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000. Use Chrome or Edge for the microphone button
(Web Speech API support varies by browser); a text box is always available
as a fallback.

API docs (FastAPI auto-generated): http://localhost:8000/docs

Drop `.mp3`/`.wav`/`.ogg` files into `static/music/` to enable "play music".

## Run with Docker

```bash
cd jarvis-web
docker build -t jarvis-web .
docker run -p 8000:8000 --env-file .env jarvis-web
```

## Deploy to Render.com (free tier)

1. Push this repo to GitHub.
2. On [render.com](https://render.com), click **New +** → **Web Service**
   and connect your repo.
3. Render will detect the `Dockerfile` automatically — choose
   **Docker** as the environment (no build/start command needed).
4. Under **Environment**, add `OPENAI_API_KEY` as a secret (optional —
   the assistant works without it, just with a more limited fallback).
5. Deploy. Render builds the image and gives you a public HTTPS URL.

Notes:
- The free tier **spins down after inactivity** and takes ~30-60s to wake
  up on the next request — a good example of a "cold start".
- Each Render instance is ephemeral: anything written to disk (e.g. a
  database) won't persist across deploys/restarts.
