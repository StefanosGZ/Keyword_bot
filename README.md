# Hourly Keyword Checker (Telegram + ntfy)

A small GitHub Actions bot that checks a web page for a keyword (or phrase) and sends a notification when it’s found.

- Runs **hourly** via GitHub Actions cron
- Fetches a target **URL**
- Searches for **NEEDLE** in the page HTML (with light normalization)
- If found, sends alerts to:
  - **Telegram** (bot message)
  - **ntfy.sh** (push notification)

---

## How it works

The bot does a simple substring search:

1. Downloads the page HTML from `URL`
2. Normalizes both the page and the keyword:
   - decodes HTML entities
   - normalizes dash variants (–, — → -)
   - collapses whitespace
3. Checks whether `NEEDLE` is contained in the page
4. If found, sends the configured `MESSAGE` with `TITLE` via Telegram + ntfy

> Note: This searches the **full HTML**, not just visible text.

---

## Repository layout

- `bot.py` — the checker + notification sender
- `.github/workflows/hourly-check.yml` — GitHub Actions workflow (runs hourly)
- `requirements.txt` — Python deps

---

## Setup (GitHub Actions)

### 1) Create a Telegram bot and chat ID

- Create a bot with **@BotFather** and copy the bot token.
- Get your chat ID (any method is fine as long as you obtain the numeric chat ID):
  - message your bot once, then read updates from the Telegram API, or
  - use a helper bot that shows your chat ID.

### 2) Add GitHub repository secrets

Go to: **Repo → Settings → Secrets and variables → Actions → New repository secret**

Add:

| Secret name | Required | Description |
|---|---:|---|
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram bot token from BotFather |
| `TELEGRAM_CHAT_ID` | ✅ | Chat ID to send messages to |
| `URL` | ✅ | Page to fetch and check |
| `NEEDLE` | ✅ | Keyword/phrase to search for |
| `TITLE` | ✅ | Notification title (used for ntfy) |
| `MESSAGE` | ✅ | Message body to send when found |
| `NTFY_TOPIC` | ✅ recommended | ntfy topic name (acts like a password) |

**Important:** `NTFY_TOPIC` should be a long random string. Anyone who guesses it can publish to your topic.

### 3) Enable Actions

Make sure GitHub Actions is enabled for the repository. The workflow runs hourly and can also be triggered manually.

---

## Manual run (GitHub)

Go to **Actions → hourly-check → Run workflow**.

---

## Run locally

### 1) Install dependencies

```bash
pip install -r requirements.txt
