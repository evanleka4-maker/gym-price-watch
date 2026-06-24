"""
Monitors r/homegym and r/powerlifting for buying-intent posts.
Emails a digest with suggested replies the user can copy-paste.
Runs automatically via the scheduler every 24h.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import time

SUBREDDITS = ["homegym", "powerlifting", "weightlifting", "crossfit"]

BUYING_KEYWORDS = [
    "best price", "where to buy", "cheapest", "good deal", "on sale",
    "vs rogue", "vs titan", "vs rep fitness", "rogue or titan",
    "price comparison", "worth it", "should i buy", "recommendations",
    "barbell recommendation", "power rack recommendation", "bumper plate",
    "home gym build", "building a home gym", "first home gym",
]

SITE_URL = "https://web-production-76350.up.railway.app"

HEADERS = {"User-Agent": "GymPriceWatch/1.0 (price comparison tool)"}


def _generate_reply(post_title, subreddit):
    title_lower = post_title.lower()

    if any(w in title_lower for w in ["barbell", "bar"]):
        item = "barbells"
        url = f"{SITE_URL}/category/Barbells"
    elif any(w in title_lower for w in ["rack", "squat stand"]):
        item = "power racks"
        url = f"{SITE_URL}/category/Power Racks"
    elif any(w in title_lower for w in ["bumper", "plate"]):
        item = "bumper plates"
        url = f"{SITE_URL}/category/Bumper Plates"
    elif any(w in title_lower for w in ["bench"]):
        item = "benches"
        url = f"{SITE_URL}/category/Benches"
    elif any(w in title_lower for w in ["kettlebell"]):
        item = "kettlebells"
        url = f"{SITE_URL}/category/Kettlebells"
    elif any(w in title_lower for w in ["rower", "bike", "cardio", "concept2"]):
        item = "cardio equipment"
        url = f"{SITE_URL}/category/Cardio"
    else:
        item = "gym equipment"
        url = SITE_URL

    replies = [
        f"I built a free price tracker that compares {item} across Rogue, Titan, Rep Fitness, and FringeSport daily — might help you decide: {url}",
        f"Prices fluctuate a lot across retailers. I track {item} daily at {url} if you want to see current prices side by side.",
        f"Check {url} — I built it specifically for this. Pulls live prices from Rogue, Titan, and Rep Fitness so you can see who's cheapest right now.",
    ]

    import hashlib
    idx = int(hashlib.md5(post_title.encode()).hexdigest(), 16) % len(replies)
    return replies[idx]


def scan_subreddit(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit=50"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        posts = resp.json()["data"]["children"]
        time.sleep(2)
        return posts
    except Exception as e:
        print(f"  [reddit] Failed to fetch r/{subreddit}: {e}")
        return []


def run():
    print("Scanning Reddit for opportunities...")
    opportunities = []
    seen_ids = set()

    for subreddit in SUBREDDITS:
        posts = scan_subreddit(subreddit)
        for post in posts:
            data = post["data"]
            post_id = data["id"]
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)

            title = data.get("title", "")
            title_lower = title.lower()

            if any(kw in title_lower for kw in BUYING_KEYWORDS):
                opportunities.append({
                    "title": title,
                    "url": f"https://reddit.com{data.get('permalink', '')}",
                    "subreddit": subreddit,
                    "score": data.get("score", 0),
                    "suggested_reply": _generate_reply(title, subreddit),
                })

    print(f"Found {len(opportunities)} opportunities.")

    if opportunities:
        from web.emailer import send_reddit_digest
        send_reddit_digest(opportunities)
        print("Digest sent.")

    return opportunities


if __name__ == "__main__":
    run()
