# Run Bot Locally (24/7 on Your Machine)

Since Railway's trial expired, you can run the bot directly on your Linux machine.

## ✅ Quick Start (Simplest Method)

```bash
cd /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel
./start_bot.sh
```

The bot will run in the background. 

**Check it's working:**
```bash
tail -f logs/bot.log
```

**Stop it:**
```bash
./stop_bot.sh
```

---

## Option 1: Using systemd (Recommended for 24/7)

### Step 1: Create systemd service file

```bash
sudo nano /etc/systemd/system/telegram-signals-bot.service
```

Paste this content:

```ini
[Unit]
Description=Signals of the Future Telegram Bot
After=network.target

[Service]
Type=simple
User=cipherghost
WorkingDirectory=/home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel
Environment="PATH=/home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel/.venv/bin"
ExecStart=/home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel/.venv/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 2: Enable and start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-signals-bot
sudo systemctl start telegram-signals-bot
```

### Step 3: Check status

```bash
sudo systemctl status telegram-signals-bot
```

### View logs

```bash
sudo journalctl -u telegram-signals-bot -f
```

---

## Option 2: Using nohup (Simpler, if you don't have sudo)

```bash
cd /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel
nohup .venv/bin/python3 main.py > bot.log 2>&1 &
```

Check if it's running:
```bash
ps aux | grep "main.py"
```

View logs:
```bash
tail -f bot.log
```

---

## Option 3: Using screen (For terminal sessions)

```bash
# Create a new screen session
screen -S telegram-bot

# Inside the screen session
cd /home/cipherghost/Documents/GitHub/AIDrivenFullyAutomatedChannel
.venv/bin/python3 main.py

# Detach: Ctrl+A then D
# Reattach: screen -r telegram-bot
```

---

## Option 4: Switch to Free Hosting (No local machine needed)

If you want to move away from Railway:

### Render (Free tier available)
- https://render.com - has free tier with 0.5GB RAM
- Deploy from GitHub like Railway

### Fly.io (Free tier available)
- https://fly.io - generous free tier
- Good for Python apps

### Heroku Alternatives
- Railway was based on Heroku
- Many similar services available

---

## Stopping the Bot

### If using systemd:
```bash
sudo systemctl stop telegram-signals-bot
```

### If using nohup:
```bash
pkill -f "main.py"
```

### If using screen:
```bash
screen -X -S telegram-bot quit
```

---

## Monitoring

Keep an eye on:
- **Logs**: `logs/bot.log` 
- **Generated images**: `generated_images/`
- **CPU usage**: `top` command

The bot uses minimal resources (~50MB RAM).
