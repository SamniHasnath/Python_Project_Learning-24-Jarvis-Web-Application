import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = "Jarvis"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(BASE_DIR, "static", "music")
