"""
Scheduler - Handles daily posting schedule
"""

import asyncio
import logging
import os
from datetime import datetime, time
import pytz
from config import MORNING_POST_TIME, EVENING_POST_TIME, TIMEZONE
from content_generator import get_content_generator
from telegram_poster import get_telegram_poster

logger = logging.getLogger(__name__)

class PostScheduler:
    """Manage scheduled posts"""
    
    def __init__(self):
        self.morning_time = self._parse_time(MORNING_POST_TIME)
        self.evening_time = self._parse_time(EVENING_POST_TIME)
        self.timezone = pytz.timezone(TIMEZONE)
        self.content_gen = get_content_generator()
        self.telegram = get_telegram_poster()
        self.running = False
    
    def _parse_time(self, time_str: str) -> time:
        """Parse time string (HH:MM format)"""
        try:
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            logger.error(f"Invalid time format: {time_str}")
            return time(10, 0)
    
    def _get_current_time(self) -> time:
        """Get current time in configured timezone"""
        now = datetime.now(self.timezone)
        return now.time()
    
    async def post_daily_content(self, time_of_day: str = "morning") -> bool:
        """
        Generate and post daily content
        
        Args:
            time_of_day: "morning" or "evening"
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Generating {time_of_day} post...")
            
            # Generate post text
            post_text = self.content_gen.generate_post_text(time_of_day)
            logger.info(f"Generated post: {post_text[:100]}...")
            
            # Generate or fetch image (with timeout to avoid hanging)
            logger.info("Generating image...")
            image_path = self.content_gen.generate_image(post_text)
            
            # Verify image exists before posting
            if image_path and os.path.exists(image_path):
                logger.info(f"✅ Image verified: {image_path}")
                with_image = True
            else:
                logger.warning(f"❌ Image not available: {image_path}")
                image_path = None
                with_image = False
            
            # Post to Telegram
            success = await self.telegram.post_message(post_text, image_path)
            
            if success:
                logger.info(f"Successfully posted {time_of_day} content with {'image' if with_image else 'text only'}")
                return True
            else:
                logger.error(f"Failed to post {time_of_day} content")
                return False
                
        except Exception as e:
            logger.error(f"Error in post_daily_content: {e}")
            return False
    
    async def run_scheduler(self):
        """Main scheduler loop"""
        self.running = True
        logger.info("Scheduler started")
        
        await self.telegram.verify_connection()
        
        last_morning_post = None
        last_evening_post = None
        
        while self.running:
            try:
                now = datetime.now(self.timezone)
                current_time = now.time()
                current_date = now.date()
                
                # Check morning post time
                if (current_time >= self.morning_time and 
                    last_morning_post != current_date):
                    logger.info(f"Time for morning post: {current_time}")
                    await self.post_daily_content("morning")
                    last_morning_post = current_date
                
                # Check evening post time
                if (current_time >= self.evening_time and 
                    last_evening_post != current_date):
                    logger.info(f"Time for evening post: {current_time}")
                    await self.post_daily_content("evening")
                    last_evening_post = current_date
                
                # Sleep for 60 seconds before checking again
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Scheduler stopped")


def get_scheduler() -> PostScheduler:
    """Get or create scheduler instance"""
    return PostScheduler()
