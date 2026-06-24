import ssl
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch(url, retries=2):
    for attempt in range(retries):
        try:
            time.sleep(random.uniform(2, 4))
            resp = requests.get(url, headers=HEADERS, timeout=(8, 20), verify=False)
            resp.raise_for_status()
            if len(resp.text) < 500:
                print(f"  [BLOCK] {url} — response too short, likely blocked")
                return None
            return BeautifulSoup(resp.text, "lxml")
        except Exception as e:
            if attempt == retries - 1:
                print(f"  [FAIL] {url} — {e}")
                return None
            time.sleep(3)
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
