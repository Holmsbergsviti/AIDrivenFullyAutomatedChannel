#!/bin/bash

# Setup script for AI-Driven Telegram Channel Bot
# This script sets up the environment and runs the bot

echo "🤖 AI-Driven Telegram Channel Setup"
echo "===================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Telegram bot token and other credentials"
fi

# Create necessary directories
mkdir -p logs generated_images

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TELEGRAM_CHANNEL_ID"
echo "   - (Optional) OPENAI_API_KEY or GROQ_API_KEY"
echo ""
echo "2. Run the bot:"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. To deploy on Heroku/Railway/PythonAnywhere, follow the README.md"
echo ""
