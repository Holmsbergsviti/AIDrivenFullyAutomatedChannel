import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME", "")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Channel Configuration
CHANNEL_TOPIC = os.getenv("CHANNEL_TOPIC", "Signals of the Future")
CHANNEL_DESCRIPTION = os.getenv("CHANNEL_DESCRIPTION", "Short notes about changes already happening — quietly. AI, behavior, money, internet culture, everyday life.\n\nNotice first.\nUnderstand later.\n\nThis is an AI-driven channel.")

# Schedule Configuration
MORNING_POST_TIME = os.getenv("MORNING_POST_TIME", "10:00")
EVENING_POST_TIME = os.getenv("EVENING_POST_TIME", "20:00")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Image Generation
USE_DALLE = os.getenv("USE_DALLE", "false").lower() == "true"
USE_UNSPLASH = os.getenv("USE_UNSPLASH", "true").lower() == "true"
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "")

# Free AI Services
USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "generated_images")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Create directories if they don't exist
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
