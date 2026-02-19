# 🤖 AI-Driven Fully Automated Telegram Channel

Automate daily posts to your Telegram channel with AI-generated content and images. Posts automatically at 10:00 and 20:00 every day with zero manual effort needed after setup.

## ✨ Features

- ✅ **Fully Automated**: Set it once and forget it
- ✅ **AI-Generated Posts**: Creates human-like, engaging content using OpenAI or Groq
- ✅ **Beautiful Images**: Generates or fetches eye-catching images for each post
- ✅ **Free Hosting**: Deploy on Heroku free tier or Railway
- ✅ **24/7 Operation**: Runs continuously without intervention
- ✅ **Customizable Schedule**: Posts at your preferred times
- ✅ **Multiple AI Services**: Works with OpenAI, Groq, DALL-E, Unsplash, or fallback content
- ✅ **Easy Setup**: Copy `.env.example` to `.env` and add your keys

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Telegram Channel ID (your channel's ID or username)
- OpenAI API Key (optional but recommended)
- Unsplash API Key (optional, for free images)

### 2. Local Setup

```bash
# Clone or navigate to the repository
cd AIDrivenFullyAutomatedChannel

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python main.py
```

### 3. Get Required Credentials

#### Telegram Bot Token
1. Open [@BotFather](https://t.me/botfather) on Telegram
2. Send `/start`
3. Send `/newbot`
4. Follow the prompts and copy your bot token
5. Add bot to your channel as an administrator

#### Telegram Channel ID
1. If you have username: Use `@your_channel_name`
2. If you need numeric ID: Use [@userinfobot](https://t.me/userinfobot) and get the channel ID

#### OpenAI API Key (Optional but recommended)
1. Go to [OpenAI API](https://platform.openai.com/api-keys)
2. Create new API key
3. Add to `.env`

#### Unsplash API Key (Optional for free images)
1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Create a new application
3. Copy Access Key and add to `.env`

## 📋 Configuration (.env)

```env
# Required
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHANNEL_ID=@your_channel_or_id
TELEGRAM_BOT_USERNAME=your_bot_username

# Optional AI
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Channel
CHANNEL_TOPIC=Your topic here
CHANNEL_DESCRIPTION=Your description

# Schedule (24-hour format)
MORNING_POST_TIME=10:00
EVENING_POST_TIME=20:00
TIMEZONE=UTC

# Images
USE_DALLE=false
USE_UNSPLASH=true
UNSPLASH_ACCESS_KEY=your_key_if_using
```

## 🌐 Free Hosting Options

### Option 1: Heroku (Recommended - Easiest)

1. Create account at [heroku.com](https://www.heroku.com)
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Deploy:

```bash
heroku login
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TELEGRAM_CHANNEL_ID=your_channel
heroku config:set OPENAI_API_KEY=your_key
# Set other variables similarly
git push heroku main
heroku logs --tail
```

### Option 2: Railway (Free tier with credits)

1. Create account at [railway.app](https://railway.app)
2. Connect your GitHub repo
3. Add environment variables in dashboard
4. Deploy automatically

### Option 3: Replit (Free)

1. Go to [replit.com](https://replit.com)
2. Create new Python project
3. Upload your files
4. Add secrets (environment variables)
5. Run with `python main.py`

### Option 4: DigitalOcean App Platform (Free tier)

1. Create account at [digitalocean.com](https://www.digitalocean.com)
2. Use App Platform with GitHub integration
3. Set environment variables
4. Deploy

### Option 5: PythonAnywhere (Free tier)

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your project
3. Create scheduled task for `python main.py`

## 📦 Project Structure

```
AIDrivenFullyAutomatedChannel/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── scheduler.py           # Scheduling logic
├── content_generator.py   # AI content & image generation
├── telegram_poster.py     # Telegram API interactions
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version for Heroku
├── logs/                 # Log files
└── generated_images/     # Generated images folder
```

## 🔧 How It Works

1. **Scheduler** checks the time every 60 seconds
2. At 10:00, generates morning post and image
3. Posts content to your Telegram channel
4. At 20:00, generates evening post and image
5. Posts content to your Telegram channel
6. Repeats daily, 24/7

## 🎨 Customization

### Change Post Times
Edit `.env`:
```env
MORNING_POST_TIME=09:00
EVENING_POST_TIME=18:00
```

### Change Topic
Edit `.env`:
```env
CHANNEL_TOPIC=Your new topic here
```

### Use Different AI Service
For Groq (faster, free tier available):
```env
USE_GROQ=true
GROQ_API_KEY=your_groq_key
```

For DALL-E images:
```env
USE_DALLE=true
USE_UNSPLASH=false
```

## 📊 Logs

Check logs to monitor bot activity:

**Local:**
```bash
tail -f logs/bot.log
```

**On Heroku:**
```bash
heroku logs --tail
```

**On Railway:**
View in dashboard

## ⚠️ Free Tier Limits

- **Heroku**: 550 free hours/month (enough for 24/7 with another free app)
- **Railway**: $5 free credits/month
- **OpenAI**: Pay-as-you-go ($0.50 free credits usually)
- **Unsplash**: 50 requests/hour on free tier
- **Groq**: Higher free tier limits

## 🐛 Troubleshooting

### Bot not posting?
1. Check bot is admin in channel: `/myid` in channel and verify access
2. Check logs: `heroku logs --tail`
3. Verify `.env` variables are set correctly
4. Test manually: `python main.py`

### "Invalid token" error?
- Verify TELEGRAM_BOT_TOKEN is correct
- Token should not have quotes in .env

### "Channel not found" error?
- Use format: `@channel_name` or numeric ID with `-100` prefix
- Verify bot is added as admin to channel

### Images not generating?
- Check if API keys are valid
- Falls back to generated images if APIs fail
- Check logs for specific errors

## 📝 Tips for Success

1. **Test locally first** before deploying
2. **Monitor the first few days** of operation
3. **Set up log notifications** for errors
4. **Rotate API keys** monthly for security
5. **Join your channel** to verify posts look good
6. **Adjust posting times** based on your audience

## 🔒 Security

- Never commit `.env` file
- Use strong, unique API keys
- Regenerate keys if leaked
- Use environment secrets on hosting platform
- Regularly check logs for suspicious activity

## 📧 Support

For issues:
1. Check logs first
2. Verify all environment variables
3. Test with local run
4. Check GitHub issues
5. Review API documentation

## 📄 License

MIT License - Feel free to use and modify

## 🎉 Happy Automating!

Your channel will now post beautiful, AI-generated content every day without your intervention. Sit back and watch your channel grow! 🚀

---

**Made with ❤️ by AI automation**
