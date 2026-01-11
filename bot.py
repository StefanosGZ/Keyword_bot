import os
import re
import sys
from html import unescape

import requests
from dotenv import load_dotenv

load_dotenv()

def normalize(s: str) -> str:
    """Decode HTML entities, normalize dash variants, and collapse whitespace."""
    s = unescape(s)
    s = s.replace("–", "-").replace("—", "-")  # normalize en/em dash
    s = re.sub(r"\s+", " ", s).strip()
    return s

def require_env(name: str) -> str:
    """Get an env var or raise a clear error."""
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing environment variable: {name}")
    return val

def send_telegram(text: str) -> None:
    token = require_env("TELEGRAM_BOT_TOKEN")
    chat_id = require_env("TELEGRAM_CHAT_ID")

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    resp = requests.post(
        api_url,
        json={"chat_id": chat_id, "text": text, "disable_web_page_preview": True},
        timeout=15,
    )
    resp.raise_for_status()

def send_ntfy(topic: str, text: str, title: str = "Keyword alert") -> None:
    # Topic is effectively a password; pick something hard to guess
    url = f"https://ntfy.sh/{topic}"
    resp = requests.post(
        url,
        data=text.encode("utf-8"),
        headers={"Title": title},
        timeout=15
    )
    resp.raise_for_status()


def main() -> None:
    url = require_env("URL")
    needle = require_env("NEEDLE")

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    r.encoding = "utf-8"
    page = r.text

    found = normalize(needle) in normalize(page)

    print("FOUND:", found)

    if found:
        tg_message = (
            require_env("MESSAGE")
        )

        send_telegram(tg_message)
        NTFY_TOPIC = os.getenv("NTFY_TOPIC", "put-your-random-topic-here")
        send_ntfy(NTFY_TOPIC, tg_message, title=require_env("TITLE"))

        print("Notifications sent.")

    sys.exit(0)

if __name__ == "__main__":
    main()
