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

    c.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            listing_id INTEGER NOT NULL,
            price REAL,
            in_stock INTEGER DEFAULT 1,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (listing_id) REFERENCES retailer_listings(id)
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
    history = get_price_history(p["id"], conn)
    conn.close()
    return {"product": dict(p), "listings": listings, "history": history}


def get_listings_with_latest_price(product_id, conn):
    from config import AFFILIATE_IDS
    rows = conn.execute("""
        SELECT rl.retailer, rl.url,
               ph.price, ph.in_stock, ph.scraped_at
        FROM retailer_listings rl
        LEFT JOIN price_history ph ON ph.listing_id = rl.id
            AND ph.id = (
                SELECT id FROM price_history
                WHERE listing_id = rl.id
                ORDER BY scraped_at DESC LIMIT 1
            )
        WHERE rl.product_id = ?
        ORDER BY ph.price ASC
    """, (product_id,)).fetchall()
    result = []
    for r in rows:
        row = dict(r)
        row["affiliate_url"] = _build_affiliate_url(row["retailer"], row["url"], AFFILIATE_IDS)
        result.append(row)
    return result


def _build_affiliate_url(retailer, url, affiliate_ids):
    aid = affiliate_ids.get(retailer, "")
    if not aid or aid.startswith("YOUR_"):
        return url
    if retailer == "rogue":
        return f"{url}?ref={aid}"
    if retailer in ("titan", "rep_fitness"):
        return f"{url}?ref={aid}"
    if retailer == "amazon":
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}tag={aid}"
    return url


def get_price_history(product_id, conn):
    rows = conn.execute("""
        SELECT rl.retailer, ph.price, ph.scraped_at
        FROM price_history ph
        JOIN retailer_listings rl ON ph.listing_id = rl.id
        WHERE rl.product_id = ?
        ORDER BY ph.scraped_at ASC
    """, (product_id,)).fetchall()
    return [dict(r) for r in rows]


def save_price(listing_id, price, in_stock=True):
    conn = get_conn()
    conn.execute(
        "INSERT INTO price_history (listing_id, price, in_stock) VALUES (?, ?, ?)",
        (listing_id, price, 1 if in_stock else 0)
    )
    conn.commit()
    conn.close()


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


def get_best_deals(limit=6):
    from config import AFFILIATE_IDS
    conn = get_conn()
    rows = conn.execute("""
        SELECT p.slug, p.name, p.category, p.image_url,
               rl.retailer, rl.url, ph.price
        FROM price_history ph
        JOIN retailer_listings rl ON ph.listing_id = rl.id
        JOIN products p ON rl.product_id = p.id
        WHERE ph.id = (
            SELECT id FROM price_history
            WHERE listing_id = rl.id
            ORDER BY scraped_at DESC LIMIT 1
        )
        AND ph.price IS NOT NULL
        ORDER BY ph.price ASC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        row = dict(r)
        row["affiliate_url"] = _build_affiliate_url(row["retailer"], row["url"], AFFILIATE_IDS)
        result.append(row)
    return result
