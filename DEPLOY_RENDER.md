# Deploy to Render (Free Tier)

Render is like Railway but with a better free tier. Your bot will run 24/7 for free.

## Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (easiest option)
3. Authorize Render to access your repositories

## Step 2: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Select your repository: `AIDrivenFullyAutomatedChannel`
3. Connect and authorize

## Step 3: Configure Service

**Name:** `signals-bot`

**Environment:** Python

**Region:** Frankfurt (or closest to you)

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python main.py
```

**Plan:** Free

## Step 4: Add Environment Variables

Click **"Environment"** and add these variables:

| Key | Value |
|-----|-------|
| `TELEGRAM_BOT_TOKEN` | `8457718874:AAFll2__BgB0e8mO7mWeY8uSNDVlHPUQ37E` |
| `TELEGRAM_CHANNEL_ID` | `@signalsOfTheFuture` |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `MORNING_POST_TIME` | `10:00` |
| `EVENING_POST_TIME` | `20:00` |
| `TIMEZONE` | `UTC` |
| `USE_DALLE` | `false` |
| `USE_UNSPLASH` | `false` |

## Step 5: Deploy

Click **"Create Web Service"**

Render will:
- Clone your repo
- Install dependencies
- Start the bot
- Keep it running 24/7

## Monitor Your Bot

1. Go to your service dashboard
2. Click **"Logs"** to see real-time logs
3. Bot will post at 10:00 and 20:00 UTC automatically

## Redeploy on Code Changes

Every time you push to GitHub, Render will automatically redeploy.

## Limits

**Render Free Tier:**
- ✅ 1 web service
- ✅ 400 compute hours/month (plenty for this bot)
- ✅ Automatic restarts if it crashes
- ✅ Custom domains (optional)
- ❌ Spins down after 15 mins of inactivity (but we have constant scheduled posts)

## Important Note About Free Tier

Render's free web services **do spin down** after 15 minutes of inactivity. However, since your bot posts every 12 hours (10:00 and 20:00 UTC), it will stay awake due to the scheduled activity.

If you want guaranteed 24/7 without any dormancy:
- Upgrade to **Render paid plan** ($7/month)
- Use a different service like **Fly.io** (more generous free tier)

## Troubleshooting

**Service won't start:**
- Check logs on Render dashboard
- Verify environment variables are set
- Make sure `requirements.txt` has all dependencies

**Bot not posting:**
- Check service logs
- Verify Telegram bot token is correct
- Ensure channel ID is correct

**Too many posts too quickly:**
- Render might restart service multiple times
- Check logs to see restart events
- If frequent, may need to upgrade plan

---

## Alternative: Fly.io (Also Free)

If Render doesn't work, try **Fly.io**:
- https://fly.io
- Better free tier (3 shared-cpu-1x 256MB VMs)
- More reliable for scheduled tasks

Would need a `fly.toml` config file instead of `render.yaml`.
