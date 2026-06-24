import requests
from bs4 import BeautifulSoup
import re
import time
import random


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            time.sleep(random.uniform(1.5, 3.5))
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            if attempt == retries - 1:
                print(f"  [FAIL] {url} — {e}")
                return None
            time.sleep(2 ** attempt)
    return None


def extract_price(text):
    if not text:
        return None
    text = str(text).replace(",", "").strip()
    match = re.search(r"\$?([\d]+\.?\d*)", text)
    if match:
        return float(match.group(1))
    return None


def json_ld_price(soup):
    import json
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, list):
                data = data[0]
            offers = data.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0]
            price = offers.get("price") or offers.get("lowPrice")
            if price:
                return float(price)
        except Exception:
            continue
    return None


def og_price(soup):
    tag = soup.find("meta", property="product:price:amount")
    if tag:
        return extract_price(tag.get("content"))
    return None
