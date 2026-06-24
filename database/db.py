import sqlite3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_PATH


def get_conn():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image_url TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS retailer_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            retailer TEXT NOT NULL,
            url TEXT NOT NULL,
            affiliate_url TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE(product_id, retailer)
        )
    """)

    conn.commit()
    conn.close()


def get_all_categories():
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT category FROM products ORDER BY category"
    ).fetchall()
    conn.close()
    return [r["category"] for r in rows]


def get_products_by_category(category):
    conn = get_conn()
    products = conn.execute(
        "SELECT * FROM products WHERE category = ? ORDER BY name",
        (category,)
    ).fetchall()
    result = []
    for p in products:
        listings = get_listings_with_latest_price(p["id"], conn)
        result.append({"product": dict(p), "listings": listings})
    conn.close()
    return result


def get_product_by_slug(slug):
    conn = get_conn()
    p = conn.execute("SELECT * FROM products WHERE slug = ?", (slug,)).fetchone()
    if not p:
        conn.close()
        return None
    listings = get_listings_with_latest_price(p["id"], conn)
    conn.close()
    return {"product": dict(p), "listings": listings, "history": []}


def get_listings_with_latest_price(product_id, conn=None):
    from config import AFFILIATE_IDS
    from scraper.cache import get_price

    close_conn = conn is None
    if close_conn:
        conn = get_conn()

    rows = conn.execute("""
        SELECT rl.id, rl.retailer, rl.url
        FROM retailer_listings rl
        WHERE rl.product_id = ?
    """, (product_id,)).fetchall()

    if close_conn:
        conn.close()

    result = []
    for r in rows:
        row = dict(r)
        cached = get_price(row["id"])
        row["price"] = cached["price"]
        row["in_stock"] = cached["in_stock"]
        row["scraped_at"] = cached["scraped_at"]
        row["affiliate_url"] = _build_affiliate_url(row["retailer"], row["url"], AFFILIATE_IDS)
        result.append(row)

    result.sort(key=lambda x: (x["price"] is None, x["price"] or 0))
    return result


def _build_affiliate_url(retailer, url, affiliate_ids):
    aid = affiliate_ids.get(retailer, "")
    if not aid or aid.startswith("YOUR_"):
        return url
    if retailer in ("rogue", "rep_fitness", "fringe"):
        return f"{url}?ref={aid}"
    if retailer == "titan":
        return f"{url}?ref={aid}"
    if retailer == "amazon":
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={aid}"
    return url


def get_all_listings():
    conn = get_conn()
    rows = conn.execute("""
        SELECT rl.id, rl.retailer, rl.url, p.name
        FROM retailer_listings rl
        JOIN products p ON rl.product_id = p.id
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def search_products(query):
    conn = get_conn()
    q = f"%{query}%"
    products = conn.execute(
        "SELECT * FROM products WHERE name LIKE ? OR description LIKE ? OR category LIKE ?",
        (q, q, q)
    ).fetchall()
    result = []
    for p in products:
        listings = get_listings_with_latest_price(p["id"], conn)
        result.append({"product": dict(p), "listings": listings})
    conn.close()
    return result


def get_best_deals(limit=50):
    from config import AFFILIATE_IDS
    from scraper.cache import get_price

    conn = get_conn()
    rows = conn.execute("""
        SELECT p.slug, p.name, p.category, p.image_url,
               rl.id as listing_id, rl.retailer, rl.url
        FROM retailer_listings rl
        JOIN products p ON rl.product_id = p.id
    """).fetchall()
    conn.close()

    deals = []
    for r in rows:
        row = dict(r)
        cached = get_price(row["listing_id"])
        if cached["price"] is None:
            continue
        row["price"] = cached["price"]
        row["affiliate_url"] = _build_affiliate_url(row["retailer"], row["url"], AFFILIATE_IDS)
        deals.append(row)

    deals.sort(key=lambda x: x["price"])
    return deals[:limit]


def get_all_products_with_prices():
    return get_best_deals(limit=500)
