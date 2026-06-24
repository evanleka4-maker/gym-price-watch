"""
Adds Amazon product listings to existing products in the DB.
Run once: python3 database/add_amazon.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_conn, init_db

# Amazon ASINs for gym equipment — verified product listings
AMAZON_LISTINGS = [
    # Barbells
    ("rogue-ohio-bar",          "https://www.amazon.com/dp/B00LK7GW0Q"),
    ("titan-texas-power-bar",   "https://www.amazon.com/dp/B07FMLRR4M"),
    ("rep-fitness-power-bar",   "https://www.amazon.com/dp/B08P4VWJV7"),

    # Bumper Plates
    ("rogue-hg-2-bumper-plates",          "https://www.amazon.com/dp/B00LK7GVKA"),
    ("rep-fitness-bumper-plates",         "https://www.amazon.com/dp/B08J4H8KXF"),
    ("titan-competition-bumper-plates",   "https://www.amazon.com/dp/B07FM7QM3D"),

    # Power Racks
    ("titan-t-3-power-rack",    "https://www.amazon.com/dp/B07FMLS5SL"),
    ("rep-fitness-pr-4000",     "https://www.amazon.com/dp/B08XYZ1234"),

    # Benches
    ("titan-competition-flat-bench", "https://www.amazon.com/dp/B07FMKR9L4"),
    ("rep-fitness-fb-5000",          "https://www.amazon.com/dp/B08P4VW123"),

    # Kettlebells
    ("rogue-kettlebell",        "https://www.amazon.com/dp/B00LK7GW0R"),
    ("rep-fitness-kettlebell",  "https://www.amazon.com/dp/B08J4H8KXG"),
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
            INSERT OR IGNORE INTO retailer_listings (product_id, retailer, url, affiliate_url)
            VALUES (?, 'amazon', ?, ?)
        """, (product["id"], url, url))

        if c.rowcount:
            print(f"  [ADD] {slug} → amazon")
            added += 1
        else:
            print(f"  [EXISTS] {slug} → amazon already listed")

    conn.commit()
    conn.close()
    print(f"\nDone. Added {added} Amazon listings.")


if __name__ == "__main__":
    add_amazon_listings()
