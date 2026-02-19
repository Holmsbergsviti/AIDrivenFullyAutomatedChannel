#!/usr/bin/env python3
"""
Test the Telegram bot connection and verify it can post to your channel
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from telegram import Bot
from telegram.error import TelegramError


async def test_connection():
    """Test bot connection"""
    print("🤖 Testing Telegram Bot Connection")
    print("=" * 50)
    
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Get bot info
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")
        print(f"   Bot ID: {me.id}")
        print(f"   Bot name: {me.first_name}")
        
        # Try to get channel info
        print(f"\n🔍 Testing channel access: {TELEGRAM_CHANNEL_ID}")
        
        try:
            chat = await bot.get_chat(TELEGRAM_CHANNEL_ID)
            print(f"✅ Channel found: {chat.title}")
            print(f"   Channel type: {chat.type}")
            
            # Check if bot is admin
            member = await bot.get_chat_member(TELEGRAM_CHANNEL_ID, me.id)
            if member.status in ['administrator', 'creator']:
                print(f"✅ Bot is {member.status} in channel")
            else:
                print(f"⚠️  Bot status in channel: {member.status}")
                print("   Please make the bot an administrator in the channel!")
                return False
                
        except TelegramError as e:
            print(f"❌ Cannot access channel: {e}")
            print("   Make sure:")
            print("   1. Bot is added to the channel")
            print("   2. Bot is an administrator")
            print("   3. Channel ID is correct (@signalsOfTheFuture)")
            return False
        
        print("\n" + "=" * 50)
        print("✅ All tests passed! Ready to automate.")
        print("\nNext steps:")
        print("1. Deploy to cloud (Railway, Heroku, or Replit)")
        print("2. Posts will start at 10:00 and 20:00 UTC")
        print("3. Check logs to verify posts are working")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_connection())
    sys.exit(0 if result else 1)
