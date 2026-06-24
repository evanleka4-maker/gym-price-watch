"""
Notifications via ntfy.sh — no account or signup needed.
Set NTFY_TOPIC in Railway env vars to whatever unique string you want.
Then visit https://ntfy.sh/YOUR_TOPIC to subscribe on any device.
"""
import os
import requests

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "gympricewatch-evanleka")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"


def _notify(title, message, priority="default", tags=None):
    try:
        headers = {
            "Title": title,
            "Priority": priority,
            "Tags": ",".join(tags or []),
        }
        requests.post(NTFY_URL, data=message.encode("utf-8"),
                      headers=headers, timeout=5)
    except Exception as e:
        print(f"[notify] Failed: {e}")


def notify_new_subscriber(email, product_name):
    _notify(
        title=f"New signup: {product_name}",
        message=f"{email} wants price alerts on {product_name}.",
        priority="high",
        tags=["bell", "moneybag"],
    )


def send_reddit_digest(opportunities):
    if not opportunities:
        return
    lines = []
    for o in opportunities:
        lines.append(f"• {o['title']}")
        lines.append(f"  {o['url']}")
        lines.append(f"  Reply: {o['suggested_reply'][:120]}...")
        lines.append("")

    _notify(
        title=f"Reddit: {len(opportunities)} opportunities found",
        message="\n".join(lines),
        priority="default",
        tags=["reddit"],
    )
