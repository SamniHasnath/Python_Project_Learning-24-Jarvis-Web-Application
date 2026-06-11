import os
import re
import random
import datetime
import xml.etree.ElementTree as ET
from urllib.parse import quote_plus

import requests

try:
    import wikipedia
    _wikipedia_ok = True
except ImportError:
    _wikipedia_ok = False

from .config import MUSIC_DIR, ASSISTANT_NAME


# ── helpers ───────────────────────────────────────────────────────────────────

def _files_in(folder, exts):
    if not os.path.isdir(folder):
        return []
    return [f for f in os.listdir(folder) if f.lower().endswith(tuple(exts))]


def _reply(text, action=None):
    return {"reply": text, "action": action}


# Names that map to a desktop application in the original assistant — these
# can't be launched from a web page, so they get a dedicated message instead
# of falling back to a Google search.
_DESKTOP_APPS = {
    "notepad", "calculator", "calc", "paint", "browser", "chrome", "edge",
    "explorer", "task manager", "vs code", "vscode", "whatsapp", "spotify",
    "telegram", "settings", "camera", "clock", "word", "excel", "powerpoint",
    "vlc", "file manager",
}


# ── greeting ──────────────────────────────────────────────────────────────────

def greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        period = "Good morning"
    elif hour < 18:
        period = "Good afternoon"
    else:
        period = "Good evening"
    return f"{period}! I am {ASSISTANT_NAME}. How can I help you?"


def greet_back():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "Good morning! How can I help you?"
    elif hour < 18:
        return "Good afternoon! How can I help you?"
    else:
        return "Good evening! How can I help you?"


# ── time / date ───────────────────────────────────────────────────────────────
# Note: this is the SERVER's clock. In a multi-user deployment the visitor's
# timezone may differ — a fuller version would read the time client-side.

def get_time():
    now = datetime.datetime.now().strftime("%I:%M %p")
    return f"The server time is {now}"


def get_date():
    today = datetime.date.today().strftime("%A, %B %d %Y")
    return f"Today is {today}"


# ── search / web (returns an open_url action for the browser) ────────────────

def search_wikipedia(query):
    if not _wikipedia_ok:
        return "Wikipedia package is not installed."
    try:
        return wikipedia.summary(query, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"That topic is ambiguous. Try one of these: {', '.join(e.options[:3])}"
    except wikipedia.exceptions.PageError:
        return "I couldn't find anything on Wikipedia for that."
    except Exception:
        return "Wikipedia search failed."


def search_google(query):
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    return _reply(f"Searching Google for {query}", {"type": "open_url", "url": url})


def play_youtube(query):
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    return _reply(f"Opening YouTube search for {query}", {"type": "open_url", "url": url})


def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    return _reply(f"Opening {url}", {"type": "open_url", "url": url})


# ── music (served from static/music, played by the browser) ──────────────────

def play_music(song_name=None):
    tracks = _files_in(MUSIC_DIR, [".mp3", ".wav", ".ogg"])
    if not tracks:
        return _reply("No music files found in the static/music folder.")
    if song_name:
        match = next((t for t in tracks if song_name.lower() in t.lower()), None)
        if not match:
            return _reply(f"Couldn't find a song matching '{song_name}'.")
        track = match
    else:
        track = tracks[0]
    return _reply(f"Playing {track}", {"type": "play_audio", "url": f"/static/music/{track}"})


def stop_music():
    return _reply("Music stopped.", {"type": "stop_audio"})


# ── weather ───────────────────────────────────────────────────────────────────

def get_weather(city):
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
        if resp.status_code == 200:
            return resp.text.strip()
        return "Couldn't fetch weather right now."
    except Exception:
        return "Weather service unavailable."


# ── jokes / quotes / news ──────────────────────────────────────────────────────

def tell_joke():
    try:
        resp = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        data = resp.json()
        return f"{data['setup']} ... {data['punchline']}"
    except Exception:
        return "Why don't scientists trust atoms? Because they make up everything!"


def get_quote():
    try:
        resp = requests.get("https://zenquotes.io/api/random", timeout=5)
        data = resp.json()
        return f"{data[0]['q']} — {data[0]['a']}"
    except Exception:
        quotes = [
            "Believe you can and you're halfway there. — Theodore Roosevelt",
            "It always seems impossible until it's done. — Nelson Mandela",
            "The secret of getting ahead is getting started. — Mark Twain",
        ]
        return random.choice(quotes)


def get_news():
    try:
        url  = "https://feeds.bbci.co.uk/news/rss.xml"
        resp = requests.get(url, timeout=5)
        root = ET.fromstring(resp.content)
        items = root.findall("./channel/item")[:5]
        headlines = [item.find("title").text for item in items if item.find("title") is not None]
        if not headlines:
            return "Couldn't fetch news right now."
        result = "Here are the top news headlines. "
        for i, h in enumerate(headlines, 1):
            result += f"{i}. {h}. "
        return result.strip()
    except Exception:
        return "Couldn't fetch news right now."


# ── timer (handled client-side by the browser) ────────────────────────────────

def _parse_duration(cmd):
    match = re.search(r'(\d+)\s*(hour|hr|minute|min|second|sec)', cmd)
    if not match:
        return None, None
    value = int(match.group(1))
    unit  = match.group(2)
    if unit.startswith("h"):
        return value * 3600, f"{value} hour{'s' if value > 1 else ''}"
    if unit.startswith("m"):
        return value * 60,   f"{value} minute{'s' if value > 1 else ''}"
    return value, f"{value} second{'s' if value > 1 else ''}"


def set_timer(cmd):
    seconds, label = _parse_duration(cmd)
    if seconds is None:
        return "Please say the duration, for example: set timer for 5 minutes."
    return _reply(
        f"Timer set for {label}. I'll let you know when it's done.",
        {"type": "set_timer", "seconds": seconds, "label": label},
    )


# ── coin flip / dice roll ──────────────────────────────────────────────────────

def flip_coin():
    result = random.choice(["Heads", "Tails"])
    return f"I flipped a coin and got {result}!"


def roll_dice(sides=6):
    result = random.randint(1, sides)
    return f"I rolled a {sides}-sided dice and got {result}!"


# ── command router ────────────────────────────────────────────────────────────

def route(command: str):
    """Returns {"reply": str, "action": dict|None}, or None to fall back to AI."""
    cmd = command.lower().strip()

    if any(w in cmd for w in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "good night"]):
        return _reply(greet_back())

    if "how are you" in cmd:
        return _reply("I'm doing great, thank you for asking! How can I help you?")

    if "your name" in cmd or "who are you" in cmd:
        return _reply("I am Jarvis, your personal AI assistant. How can I help you?")

    if "what can you do" in cmd or "can you do" in cmd or "help" in cmd:
        return _reply(
            "I can tell the time, date, news headlines, quotes, jokes, weather, "
            "set timers, flip a coin, roll dice, search Google or Wikipedia, "
            "play YouTube, and play music from my library. Just ask!"
        )

    if "set timer" in cmd or "start timer" in cmd or "timer for" in cmd:
        return set_timer(cmd)

    if "time" in cmd:
        return _reply(get_time())

    if "date" in cmd:
        return _reply(get_date())

    if "battery" in cmd or "system info" in cmd or "cpu" in cmd or "ram" in cmd \
            or "memory" in cmd or "ip address" in cmd or "my ip" in cmd:
        return _reply("That's only available in the desktop version of Jarvis.")

    if "flip" in cmd and "coin" in cmd:
        return _reply(flip_coin())

    if "roll" in cmd and "dice" in cmd:
        match = re.search(r'(\d+)', cmd)
        sides = int(match.group(1)) if match else 6
        return _reply(roll_dice(sides))

    if "quote" in cmd or "motivate" in cmd or "inspire" in cmd:
        return _reply(get_quote())

    if "news" in cmd or "headlines" in cmd:
        return _reply(get_news())

    if "wikipedia" in cmd or "who is" in cmd or "what is" in cmd:
        query = (cmd.replace("wikipedia", "")
                    .replace("who is", "")
                    .replace("what is", "")
                    .strip())
        return _reply(search_wikipedia(query))

    if "play" in cmd and ("youtube" in cmd or "song" in cmd or "music" in cmd):
        query = (cmd.replace("play", "")
                    .replace("on youtube", "")
                    .replace("youtube", "")
                    .replace("song", "")
                    .replace("music", "")
                    .strip())
        return play_youtube(query) if "youtube" in cmd or query else play_music(query or None)

    if "stop music" in cmd or "pause music" in cmd:
        return stop_music()

    if "weather" in cmd:
        city = (cmd.replace("weather", "")
                   .replace(" in ", "")
                   .replace(" for ", "")
                   .strip())
        return _reply(get_weather(city if city else "London"))

    if "joke" in cmd:
        return _reply(tell_joke())

    if "open" in cmd:
        target = cmd.replace("open", "").strip()
        if "." in target or target.startswith("www"):
            return open_website(target)
        if target in _DESKTOP_APPS:
            return _reply("Opening desktop apps isn't available in the web version. Try asking me to open a website.")
        if target:
            return search_google(target)
        return _reply("What would you like me to open?")

    if "search" in cmd or "google" in cmd:
        query = (cmd.replace("search", "")
                    .replace("google", "")
                    .replace("for", "")
                    .strip())
        return search_google(query)

    if any(w in cmd for w in ["bye", "exit", "quit", "goodbye"]):
        return _reply("Goodbye! Have a great day.", {"type": "end_session"})

    return None  # fall through to AI
