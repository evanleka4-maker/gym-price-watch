import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_all_listings
from scraper import cache
from scraper import rogue, titan, rep_fitness

SCRAPERS = {
    "rogue": rogue.scrape_price,
    "titan": titan.scrape_price,
    "rep_fitness": rep_fitness.scrape_price,
}


def run_all():
    listings = get_all_listings()
    print(f"Scraping {len(listings)} listings...")

    for listing in listings:
        retailer = listing["retailer"]
        scraper = SCRAPERS.get(retailer)
        if not scraper:
            continue

        print(f"  [{retailer}] {listing['name']}...")
        try:
            price, in_stock = scraper(listing["url"])
            cache.set_price(listing["id"], price, in_stock)
            status = f"${price:.2f}" if price else "no price"
            print(f"    → {status}")
        except Exception as e:
            print(f"    → ERROR: {e}")

    print("Scrape complete.")
