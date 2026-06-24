"""
Adds Amazon product listings to existing products in the DB.
Run once: python3 database/add_amazon.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_conn, init_db

# Amazon ASINs — manually verified against amazon.com
# Tag: gympricewatch-20
AMAZON_LISTINGS = [
    # Barbells
    ("rogue-ohio-bar",        "https://www.amazon.com/dp/B00LK7GW0Q?tag=gympricewatch-20"),
    ("rogue-hg-2-bumper-plates", "https://www.amazon.com/dp/B00LK7GVKA?tag=gympricewatch-20"),
]


def add_amazon_listings():
    init_db()
    conn = get_conn()
    c = conn.cursor()
    added = 0

    for slug, url in AMAZON_LISTINGS:
        product = c.execute(
            "SELECT id FROM products WHERE slug = ?", (slug,)
        ).fetchone()

        if not product:
            print(f"  [SKIP] No product found for slug: {slug}")
            continue

        c.execute("""
            INSERT OR REPLACE INTO retailer_listings (product_id, retailer, url, affiliate_url)
            VALUES (?, 'amazon', ?, ?)
        """, (product["id"], url, url))

        if c.rowcount:
            print(f"  [ADD] {slug} → amazon")
            added += 1

    conn.commit()
    conn.close()
    print(f"\nDone. Added {added} Amazon listings.")


if __name__ == "__main__":
    add_amazon_listings()
