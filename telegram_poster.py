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
            # Truncate caption if too long for Telegram
            if image_path and len(text) > 1024:
                text = text[:1020] + "..."
            if image_path:
                logger.info(f"📸 Attempting to send photo from {image_path}")
                with open(image_path, "rb") as photo:
                    result = await self.bot.send_photo(
                        chat_id=self.channel_id,
                        photo=photo,
                        caption=text
                    )
                logger.info(f"✅ Posted photo message to {self.channel_id} (message ID: {result.message_id})")
            else:
                logger.info(f"📝 Attempting to send text message")
                result = await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=text
                )
                logger.info(f"✅ Posted text message to {self.channel_id} (message ID: {result.message_id})")
            
            return True
            
        except FileNotFoundError as e:
            logger.error(f"❌ Image file not found: {image_path} - {e}")
            # Try posting text-only if image is missing
            try:
                await self.bot.send_message(chat_id=self.channel_id, text=text)
                logger.info(f"✅ Posted text-only fallback")
                return True
            except Exception as e2:
                logger.error(f"❌ Fallback also failed: {e2}")
                return False
        except TelegramError as e:
            logger.error(f"❌ Telegram error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error while posting: {e}")
            import traceback
            logger.error(traceback.format_exc())
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
