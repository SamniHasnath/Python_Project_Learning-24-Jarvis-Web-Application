[# Jarvis Web

A browser-based version of the Jarvis assistant. The "brain" (command
routing + OpenAI fallback) runs as a small FastAPI service; speech-to-text
and text-to-speech happen in the browser via the Web Speech API.

This sits alongside `jarvis-assistant/`, the original terminal/desktop
version, which is left untouched.

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
# Python_Project_Learning-24-Jarvis-Web-Application
](https://jarvisweb-ryua.onrender.com)
