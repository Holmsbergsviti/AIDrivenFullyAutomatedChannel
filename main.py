"""
Main Application - AI-Driven Automated Telegram Channel Poster
Runs 24/7 and posts at scheduled times (10:00 and 20:00 by default)
"""

import asyncio
import logging
import sys
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import scheduler
from scheduler import get_scheduler
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, OPENAI_API_KEY


def validate_configuration():
    """Validate that all required configuration is set"""
    errors = []
    
    if not TELEGRAM_BOT_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN is not set")
    if not TELEGRAM_CHANNEL_ID:
        errors.append("❌ TELEGRAM_CHANNEL_ID is not set")
    if not OPENAI_API_KEY:
        errors.append("⚠️  OPENAI_API_KEY is not set (some features may not work)")
    
    if errors:
        logger.error("Configuration validation failed:")
        for error in errors:
            logger.error(error)
        
        if len(errors) > 1 or "not set" in str(errors[0]):
            logger.error("\nPlease set up your .env file with required values")
            return False
    
    logger.info("✅ Configuration validated successfully")
    return True


async def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("🤖 AI-Driven Telegram Channel Automation")
    logger.info("=" * 60)
    
    # Validate configuration
    if not validate_configuration():
        sys.exit(1)
    
    # Initialize scheduler
    scheduler = get_scheduler()
    
    # Start scheduler
    try:
        await scheduler.run_scheduler()
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        scheduler.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Application terminated")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)
