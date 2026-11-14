# Signals of the Future — an AI-run Telegram channel

A Python service that runs a Telegram channel end to end with no human in the loop. Twice a day it
asks an LLM to write a short, observational post in a fixed editorial voice, picks or renders an
image to go with it, and publishes both to the channel through the Telegram Bot API.

**Live channel:** [t.me/signalsOfTheFuture](https://t.me/signalsOfTheFuture)

## How it works

```
asyncio scheduler (60 s tick, timezone-aware)
        │  morning / evening slot due and not yet posted today?
        ▼
ContentGenerator.generate_post_text()      Groq (Llama 3.3 70B) | OpenAI (by config) → curated fallback
        │
ContentGenerator.generate_image()          DALL·E 3 | Unsplash | Pillow-rendered card (by config)
        │
TelegramPoster.post_message()              send_photo (caption ≤ 1024 chars) → text-only fallback
```

- **Scheduling** — `scheduler.py` runs an `asyncio` loop that checks the clock in the configured
  `pytz` timezone every 60 seconds and remembers the last date each slot fired, so a restart or a
  slow tick never double-posts and a missed slot still fires once later that day.
- **Prompting** — one prompt defines the channel's voice (observational, short lines, ends on a
  question rather than a call to action) with few-shot examples of real posts, sent with a
  dedicated system message at `temperature=0.9`.
- **Graceful degradation** — every provider call is wrapped: if the LLM call fails the bot falls
  back to a curated set of posts in the same voice, and if the image step fails (or the file is
  missing) it publishes the post as text only. With no image provider configured it draws an image
  card locally with Pillow, so the channel keeps posting even with no API keys at all.
- **Hosting** — `main.py` starts a tiny Flask health endpoint on `$PORT` next to the bot so it can
  run on free web-service tiers that require an HTTP port (Render, Fly.io). Config for both is in
  `render.yaml` and `fly.toml`.

## Tech stack

Python 3 · asyncio · python-telegram-bot 20 · OpenAI SDK · Groq SDK · Unsplash API · Pillow ·
Flask · pytz · python-dotenv

## Project structure

| File | Role |
|---|---|
| `main.py` | Entry point: config validation, logging, health endpoint, starts the scheduler |
| `scheduler.py` | Timezone-aware daily posting loop |
| `content_generator.py` | Post text (Groq / OpenAI / fallback) and image (DALL·E / Unsplash / Pillow) |
| `telegram_poster.py` | Sends photo or text posts, verifies the bot can reach the channel |
| `config.py` | Reads every setting from the environment |
| `generate_avatar.py` | Draws the channel avatar |
| `test_bot.py`, `check_deployment.py` | Manual checks for credentials and a deployed instance |

## Run it locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # then fill in the values below
python main.py
```

The bot must be an **administrator** of the channel with permission to post.

| Variable | Required | Purpose |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | yes | Token from [@BotFather](https://t.me/botfather) |
| `TELEGRAM_CHANNEL_ID` | yes | `@channel_name` or numeric `-100…` id |
| `USE_GROQ`, `GROQ_API_KEY` | no | Use Llama 3.3 70B on Groq for text |
| `OPENAI_API_KEY` | no | GPT text and, with `USE_DALLE=true`, DALL·E 3 images |
| `USE_UNSPLASH`, `UNSPLASH_ACCESS_KEY` | no | Stock photos instead of generated images |
| `CHANNEL_TOPIC` | no | What the posts are about |
| `MORNING_POST_TIME`, `EVENING_POST_TIME`, `TIMEZONE` | no | Schedule, default `10:00` / `20:00` `UTC` |

## Deploying

Step-by-step guides: [`DEPLOY_RENDER.md`](DEPLOY_RENDER.md) (recommended),
[`HOSTING_OPTIONS.md`](HOSTING_OPTIONS.md) for Fly.io and others, and
[`CHANNEL_SETUP.md`](CHANNEL_SETUP.md) for creating the channel and bot.

## Author

Vladislav Salii · MIT License
