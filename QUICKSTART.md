# 🚀 Quick Start Guide

## 5-Minute Setup for Lazy Automation

### Step 1: Get Your Credentials (2 min)

**Telegram Bot Token:**
1. Open [@BotFather](https://t.me/botfather)
2. Send `/newbot`
3. Follow prompts, copy the token

**Your Channel ID:**
- If you have a username: `@channelname`
- Otherwise: Send a message to your channel, forward to [@userinfobot](https://t.me/userinfobot)

### Step 2: Configure (.env file)

```bash
# Open and edit .env
nano .env  # or use your editor
```

Minimum required:
```
TELEGRAM_BOT_TOKEN=123456789:ABCDEFGHijklmnopqrstuvwxyzABCD
TELEGRAM_CHANNEL_ID=@your_channel_name
CHANNEL_TOPIC=Your topic here
```

Optional (for AI-generated content):
- Get key from [OpenAI](https://platform.openai.com) - Free $5 credit
- OR get from [Groq](https://console.groq.com) - Very generous free tier

### Step 3: Test Locally (1 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

Wait for "Scheduler started" message. The bot will post at 10:00 and 20:00.

### Step 4: Deploy to Cloud (2 min)

**Easiest: Railway**
1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repo
5. Add environment variables (copy from .env)
6. Click Deploy - Done! 🎉

**Or: Heroku**
```bash
heroku login
heroku create your-app-name
# Set environment variables (see DEPLOYMENT.md)
git push heroku main
```

---

## What Happens Now

✅ Every day at 10:00:
- AI generates engaging morning post
- Creates or fetches beautiful image
- Posts to your channel

✅ Every day at 20:00:
- AI generates evening post
- Creates or fetches different image
- Posts to your channel

✅ Runs 24/7:
- No intervention needed
- Self-healing on errors
- Logs everything

---

## Customization (Optional)

### Change posting times
Edit `.env`:
```
MORNING_POST_TIME=09:00
EVENING_POST_TIME=18:00
```

### Change timezone
```
TIMEZONE=Europe/Paris
```

### Use different AI
```
USE_GROQ=true
GROQ_API_KEY=gsk_xxx
```

---

## Verify It's Working

1. **Check logs:**
   ```bash
   # Local
   tail -f logs/bot.log
   
   # Heroku
   heroku logs --tail
   
   # Railway
   View in dashboard
   ```

2. **Look at channel** - Should post at 10:00 and 20:00

3. **Check `/logs` folder** - See generated images and activity

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Telegram token invalid"
- Get a new one from @BotFather
- Make sure bot is admin in channel
- Ensure token is copied correctly (no quotes or spaces)

### No posts appearing
1. Check bot is admin in channel: `/myid` command in channel
2. Check logs for errors
3. Verify CHANNEL_TOPIC is set
4. Test with `python main.py`

### Images not generating
- Fallback to text-only posts (still works!)
- Add Unsplash key for free images
- Add OpenAI key for AI-generated images

---

## Support Resources

📖 **Full Documentation**: See `README.md`
🌐 **Deployment Guide**: See `DEPLOYMENT.md`
🔧 **Troubleshooting**: Check `logs/bot.log`

---

**That's it! Your channel now posts 730+ times per year without your help!** 🎉
