"""
Seed the database with the initial product catalog.
Run once: python database/seed.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_conn, init_db
from config import AFFILIATE_IDS


def affiliate_url(retailer, base_url):
    aid = AFFILIATE_IDS.get(retailer, "")
    if retailer == "rogue":
        return f"{base_url}?ref={aid}"
    if retailer == "titan":
        return f"{base_url}?sscid={aid}"
    if retailer == "rep_fitness":
        return f"{base_url}?ref={aid}"
    if retailer == "amazon":
        return f"{base_url}&tag={aid}"
    return base_url


CATALOG = [
    # ── BARBELLS ─────────────────────────────────────────────────────────────
    {
        "slug": "rogue-ohio-bar",
        "name": "Rogue Ohio Bar",
        "category": "Barbells",
        "description": "The gold standard 20kg men's Olympic barbell. 190k PSI tensile strength, dual knurl marks.",
        "image_url": "https://assets.roguefitness.com/f_auto,q_auto,fl_progressive,b_rgb:f8f8f8/catalog/product/cache/default/ba0bff5fb2bd186e8b0d0d63a8d7697a/o/h/ohio_bar_v2_main_1_0016.jpg",
        "retailers": {
            "rogue": "https://www.roguefitness.com/the-ohio-bar",
        }
    },
    {
        "slug": "titan-texas-power-bar",
        "name": "Titan Texas Power Bar",
        "category": "Barbells",
        "description": "29mm power bar with aggressive knurl and 210k PSI tensile strength.",
        "image_url": "",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/texas-power-bar",
        }
    },
    {
        "slug": "rep-fitness-power-bar",
        "name": "Rep Fitness Power Bar",
        "category": "Barbells",
        "description": "29mm power bar, dual knurl, 200k PSI tensile strength. Great value.",
        "image_url": "",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-power-bar",
        }
    },
    # ── BUMPER PLATES ─────────────────────────────────────────────────────────
    {
        "slug": "rogue-hg-2-bumper-plates",
        "name": "Rogue HG 2.0 Bumper Plates",
        "category": "Bumper Plates",
        "description": "High-quality virgin rubber bumper plates. Sold in pairs.",
        "image_url": "",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-hg-2-0-bumper-plates",
        }
    },
    {
        "slug": "titan-competition-bumper-plates",
        "name": "Titan Competition Bumper Plates",
        "category": "Bumper Plates",
        "description": "Steel insert, low bounce competition-style bumpers.",
        "image_url": "",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/competition-bumper-plates",
        }
    },
    {
        "slug": "rep-fitness-bumper-plates",
        "name": "Rep Fitness Bumper Plates",
        "category": "Bumper Plates",
        "description": "Virgin rubber bumper plates with steel insert. Best value in class.",
        "image_url": "",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-black-bumper-plates",
        }
    },
    # ── POWER RACKS ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-rml-390f",
        "name": "Rogue RML-390F Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge steel, foldable monster rack. 1000lb rated.",
        "image_url": "",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rml-390f-fold-back-wall-mount-power-rack",
        }
    },
    {
        "slug": "titan-t-3-power-rack",
        "name": "Titan T-3 Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge steel rack. Most popular budget rack on the market.",
        "image_url": "",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/t-3-power-rack",
        }
    },
    {
        "slug": "rep-fitness-pr-4000",
        "name": "Rep Fitness PR-4000 Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge steel, modular rack system with many attachments.",
        "image_url": "",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/pr-4000-power-rack",
        }
    },
    # ── BENCHES ──────────────────────────────────────────────────────────────
    {
        "slug": "rogue-utility-bench-20",
        "name": "Rogue Utility Bench 2.0",
        "category": "Benches",
        "description": "Heavy-duty flat utility bench. 1000lb capacity.",
        "image_url": "",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-utility-bench-2-0",
        }
    },
    {
        "slug": "titan-competition-flat-bench",
        "name": "Titan Competition Flat Bench",
        "category": "Benches",
        "description": "IPF legal competition bench. 1200lb capacity.",
        "image_url": "",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/competition-flat-bench",
        }
    },
    {
        "slug": "rep-fitness-fb-5000",
        "name": "Rep Fitness FB-5000 Flat Bench",
        "category": "Benches",
        "description": "Commercial-grade flat bench with slight decline. IPF competition spec.",
        "image_url": "",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-flat-bench-fb-5000",
        }
    },
    # ── KETTLEBELLS ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-kettlebell",
        "name": "Rogue Kettlebell",
        "category": "Kettlebells",
        "description": "Single cast iron kettlebell. Multiple weights available.",
        "image_url": "",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-kettlebells",
        }
    },
    {
        "slug": "rep-fitness-kettlebell",
        "name": "Rep Fitness Cast Iron Kettlebell",
        "category": "Kettlebells",
        "description": "Single-piece cast iron, powder coated. Multiple weights.",
        "image_url": "",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-cast-iron-kettlebells",
        }
    },
    # ── PULL-UP BARS ─────────────────────────────────────────────────────────
    {
        "slug": "rogue-monster-lite-pull-up-bar",
        "name": "Rogue Monster Lite Pull-Up System",
        "category": "Pull-Up Bars",
        "description": "Multi-grip pull-up bar for Monster Lite racks.",
        "image_url": "",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-monster-lite-pull-up-system",
        }
    },
    {
        "slug": "titan-multi-grip-pull-up-bar",
        "name": "Titan Multi-Grip Pull-Up Bar",
        "category": "Pull-Up Bars",
        "description": "Multiple grip positions, fits 2x2 and 3x3 uprights.",
        "image_url": "",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/multi-grip-pull-up-bar",
        }
    },
]


def seed():
    init_db()
    conn = get_conn()
    c = conn.cursor()

    for item in CATALOG:
        c.execute("""
            INSERT OR IGNORE INTO products (slug, name, category, description, image_url)
            VALUES (?, ?, ?, ?, ?)
        """, (item["slug"], item["name"], item["category"],
              item["description"], item.get("image_url", "")))

        product_id = c.execute(
            "SELECT id FROM products WHERE slug = ?", (item["slug"],)
        ).fetchone()["id"]

        for retailer, url in item["retailers"].items():
            aff_url = affiliate_url(retailer, url)
            c.execute("""
                INSERT OR IGNORE INTO retailer_listings (product_id, retailer, url, affiliate_url)
                VALUES (?, ?, ?, ?)
            """, (product_id, retailer, url, aff_url))

    conn.commit()
    conn.close()
    print(f"Seeded {len(CATALOG)} products.")


if __name__ == "__main__":
    seed()
