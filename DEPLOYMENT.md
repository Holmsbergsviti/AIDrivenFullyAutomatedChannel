# Deployment guide for free hosting platforms

## Heroku (Recommended - Most Stable)

### Prerequisites
- Heroku account (free)
- Heroku CLI installed
- Git repository

### Steps

```bash
# 1. Login to Heroku
heroku login

# 2. Create Heroku app
heroku create your-unique-app-name

# 3. Set environment variables
heroku config:set TELEGRAM_BOT_TOKEN="your_token"
heroku config:set TELEGRAM_CHANNEL_ID="@your_channel"
heroku config:set CHANNEL_TOPIC="Your Topic"
heroku config:set OPENAI_API_KEY="your_key"

# 4. Deploy
git push heroku main

# 5. View logs
heroku logs --tail

# 6. Check status
heroku ps
```

### Keep Free Dyno Awake
Free Heroku dynos sleep after 30 mins of inactivity. Our bot keeps running even on free tier.

---

## Railway (Very Easy)

### Steps

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose this repository
6. Add variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
   - `CHANNEL_TOPIC`
   - `OPENAI_API_KEY` (optional)
7. Click "Deploy"
8. Monitor in dashboard

---

## Replit (Easiest)

### Steps

1. Go to [replit.com](https://replit.com)
2. Click "Create" → "New Repl"
3. Choose "Python"
4. Upload all files
5. Add secrets (click lock icon):
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`
   - Others as needed
6. Click "Run" → `python main.py`
7. Keep tab open (or get Replit Pro for 24/7)

---

## PythonAnywhere (Good for scheduled tasks)

### Steps

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Files" tab
3. Upload all files to your home directory
4. Create virtual environment in Web tab
5. Bash console:
   ```bash
   pip install -r requirements.txt
   ```
6. Go to "Tasks" tab
7. Create scheduled task:
   - Command: `/usr/bin/python3.10 /home/username/main.py`
   - Frequency: Every day at 00:00
8. Keep it running

---

## DigitalOcean App Platform

### Steps

1. Go to [digitalocean.com](https://www.digitalocean.com)
2. Click "Create" → "Apps"
3. Connect GitHub
4. Choose this repository
5. Configure:
   - Build command: `pip install -r requirements.txt`
   - Run command: `python main.py`
6. Add environment variables
7. Click "Deploy"

---

## Glitch (Very Easy, But Limited)

### Steps

1. Go to [glitch.com](https://glitch.com)
2. Create new project
3. Upload files
4. Add `.env` with credentials
5. Update `Procfile`
6. Keep project open

---

## Cost Comparison (Monthly)

| Platform | Cost | Notes |
|----------|------|-------|
| Heroku | Free | 550 free hours/month |
| Railway | $5 credits | Good for light use |
| Replit | Free | Keep tab open |
| PythonAnywhere | Free | Limited features |
| DigitalOcean | $5+ | Most reliable |
| Glitch | Free | Limited |

---

## Troubleshooting Deployments

### App keeps crashing
- Check logs for errors
- Verify environment variables are set
- Check API keys are valid
- Ensure Telegram token is correct

### App starts but doesn't post
- Verify bot is admin in channel
- Check timezone is correct
- Look at scheduled times
- Review logs for errors

### Out of memory
- Switch to Python 3.11 (lighter)
- Remove unused dependencies
- Deploy to Railway or DigitalOcean

---

## Monitoring & Maintenance

### Set up alerts
- Most platforms have built-in alerting
- Set email notifications for crashes

### Regular checks
- Review logs weekly
- Check API quotas
- Monitor bot activity

### Backup strategy
- Keep `.env` secure
- Regular git commits
- Document any custom changes
