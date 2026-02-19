#!/bin/bash
# Start the Telegram bot and keep it running

cd /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel

# Create logs directory if it doesn't exist
mkdir -p logs
mkdir -p generated_images

# Run the bot in the background
nohup /bin/python3 main.py > logs/bot_startup.log 2>&1 &

# Get the PID
BOT_PID=$!
echo $BOT_PID > .bot_pid

echo "🤖 Bot started with PID: $BOT_PID"
echo "📝 Check logs with: tail -f logs/bot.log"
echo "🛑 Stop bot with: kill $BOT_PID or run stop_bot.sh"
