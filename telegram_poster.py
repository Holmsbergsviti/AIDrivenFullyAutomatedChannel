"""
Telegram Poster - Handles posting to Telegram channel
"""

import logging
from typing import Optional
from telegram import Bot
from telegram.error import TelegramError
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

logger = logging.getLogger(__name__)

class TelegramPoster:
    """Handle Telegram channel posting"""
    
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.channel_id = TELEGRAM_CHANNEL_ID
    
    async def post_message(self, text: str, image_path: Optional[str] = None) -> bool:
        """
        Post message to Telegram channel
        
        Args:
            text: Message text
            image_path: Optional path to image file
            
        Returns:
            Success status
        """
        try:
            if image_path:
                with open(image_path, "rb") as photo:
                    await self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=photo,
                        caption=text,
                        parse_mode="HTML"
                    )
                logger.info(f"Posted message with image to {self.channel_id}")
            else:
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=text,
                    parse_mode="HTML"
                )
                logger.info(f"Posted text message to {self.channel_id}")
            
            return True
            
        except TelegramError as e:
            logger.error(f"Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error while posting: {e}")
            return False
    
    async def verify_connection(self) -> bool:
        """Verify bot connection and channel access"""
        try:
            me = await self.bot.get_me()
            logger.info(f"Bot verified: {me.username}")
            return True
        except Exception as e:
            logger.error(f"Failed to verify bot connection: {e}")
            return False


def get_telegram_poster() -> TelegramPoster:
    """Get or create Telegram poster instance"""
    return TelegramPoster()
