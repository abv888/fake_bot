import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Admin user IDs (optional)
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(','))) if os.getenv("ADMIN_IDS") else []

# Conference date and time
CONFERENCE_DATE = "June 15"
CONFERENCE_TIME = "7:00 PM"  # You can adjust this

# Database settings (if you want to use a database)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "casino_guide_bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Webhook settings (if you want to use a webhook instead of polling)
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", f"/webhook/{BOT_TOKEN}")
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Webhook server settings
WEBAPP_HOST = os.getenv("WEBAPP_HOST", "localhost")
WEBAPP_PORT = int(os.getenv("WEBAPP_PORT", 8000))