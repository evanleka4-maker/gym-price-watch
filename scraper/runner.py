"""
Scrapes all listings and saves prices to the database.
Runs automatically via the scheduler, or manually: python scraper/runner.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_all_listings, save_price, get_conn
from scraper import rogue, titan, rep_fitness

SCRAPERS = {
    "rogue": rogue.scrape_price,
    "titan": titan.scrape_price,
    "rep_fitness": rep_fitness.scrape_price,
}


def run_all():
    listings = get_all_listings()
    print(f"Scraping {len(listings)} listings...")

    success, failed = 0, 0
    for listing in listings:
        retailer = listing["retailer"]
        scraper = SCRAPERS.get(retailer)
        if not scraper:
            continue

        print(f"  [{retailer}] {listing['name']}...")
        try:
            price, in_stock = scraper(listing["url"])
            save_price(listing["id"], price, in_stock)
            status = f"${price:.2f}" if price else "no price"
            stock = "in stock" if in_stock else "OUT OF STOCK"
            print(f"    → {status} / {stock}")
            success += 1
        except Exception as e:
            print(f"    → ERROR: {e}")
            failed += 1

    print(f"\nDone. {success} succeeded, {failed} failed.")


if __name__ == "__main__":
    run_all()
