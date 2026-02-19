#!/bin/bash
# Stop the Telegram bot

if [ -f /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel/.bot_pid ]; then
    BOT_PID=$(cat /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel/.bot_pid)
    kill $BOT_PID 2>/dev/null
    rm /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel/.bot_pid
    echo "🛑 Bot stopped (PID: $BOT_PID)"
else
    echo "Bot PID file not found. Killing any running instances..."
    pkill -f "python3 main.py"
    echo "🛑 Done"
fi
