import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"

LIBRARY_BASE_URL = (os.getenv("BASE_URL", "https://flibusta.is")).rstrip("/")
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_BOT_NAME = os.getenv("TG_BOT_NAME")

TG_BOT_WEBHOOK_BASE_URL = os.getenv("TG_BOT_WEBHOOK_BASE_URL")
TG_BOT_WEBHOOK_PATH = os.getenv("TG_BOT_WEBHOOK_PATH", "/webhook")
TG_BOT_WEBHOOK_SECRET = os.getenv("TG_BOT_WEBHOOK_SECRET", None)

WEB_SERVER_HOST = os.environ.get("WEB_SERVER_HOST", "0.0.0.0")
WEB_SERVER_PORT = int(os.environ.get("WEB_SERVER_PORT", 8000))

POSTGRES_DB = os.getenv("POSTGRES_DB", "flibusta_bot")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
