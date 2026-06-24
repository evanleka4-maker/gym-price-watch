"""
Seed the database with the initial product catalog.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_conn, init_db
from config import AFFILIATE_IDS


def affiliate_url(retailer, base_url):
    aid = AFFILIATE_IDS.get(retailer, "")
    if not aid or aid.startswith("YOUR_"):
        return base_url
    if retailer in ("rogue", "rep_fitness", "fringe"):
        return f"{base_url}?ref={aid}"
    if retailer == "titan":
        return f"{base_url}?ref={aid}"
    if retailer == "amazon":
        sep = "&" if "?" in base_url else "?"
        return f"{base_url}{sep}tag={aid}"
    return base_url


CATALOG = [
    # ── BARBELLS ─────────────────────────────────────────────────────────────
    {
        "slug": "rogue-ohio-bar",
        "name": "Rogue Ohio Bar",
        "category": "Barbells",
        "description": "The gold standard 20kg men's Olympic barbell. 190k PSI tensile strength, dual knurl marks.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/the-ohio-bar",
        }
    },
    {
        "slug": "rogue-ohio-deadlift-bar",
        "name": "Rogue Ohio Deadlift Bar",
        "category": "Barbells",
        "description": "27mm diameter, extra whip for max pulls. The deadlift bar of choice for competitive lifters.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/ohio-deadlift-bar",
        }
    },
    {
        "slug": "rogue-bella-bar",
        "name": "Rogue Bella Bar 2.0",
        "category": "Barbells",
        "description": "15kg women's Olympic barbell. 25mm diameter, dual knurl marks.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/bella-bar-2-0",
        }
    },
    {
        "slug": "titan-texas-power-bar",
        "name": "Titan Texas Power Bar",
        "category": "Barbells",
        "description": "29mm power bar with aggressive knurl. 210k PSI tensile strength.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/texas-power-bar",
        }
    },
    {
        "slug": "titan-olympic-bar",
        "name": "Titan Olympic Weightlifting Bar",
        "category": "Barbells",
        "description": "20kg Olympic bar with center knurl, 190k PSI tensile strength.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/olympic-weightlifting-bar",
        }
    },
    {
        "slug": "rep-fitness-power-bar",
        "name": "Rep Fitness Power Bar",
        "category": "Barbells",
        "description": "29mm power bar, dual knurl, 200k PSI tensile strength.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-power-bar",
        }
    },
    {
        "slug": "rep-fitness-apache-bar",
        "name": "Rep Fitness Apache Bar",
        "category": "Barbells",
        "description": "Multi-purpose 20kg Olympic bar. Great entry-level bar.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-apache-bar",
        }
    },
    {
        "slug": "fringe-budget-bar",
        "name": "FringeSport Wonder Bar V2",
        "category": "Barbells",
        "description": "Affordable all-purpose 20kg barbell. Best bang-for-buck entry bar.",
        "retailers": {
            "fringe": "https://www.fringesport.com/products/wonder-bar-olympic-barbell",
        }
    },

    # ── SPECIALTY BARS ───────────────────────────────────────────────────────
    {
        "slug": "rogue-safety-squat-bar",
        "name": "Rogue Safety Squat Bar",
        "category": "Specialty Bars",
        "description": "Camber bar with padded yoke. Reduces shoulder strain during squats.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-safety-squat-bar",
        }
    },
    {
        "slug": "titan-safety-squat-bar",
        "name": "Titan Safety Squat Bar",
        "category": "Specialty Bars",
        "description": "Padded yoke SSB. Compare pricing vs Rogue on the same movement.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/safety-squat-bar",
            "rep_fitness": "https://repfitness.com/products/rep-safety-squat-bar",
        }
    },
    {
        "slug": "rogue-trap-bar",
        "name": "Rogue TB-2 Trap Bar",
        "category": "Specialty Bars",
        "description": "Open-ended hex bar. Dual handle heights, 1500lb capacity.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-tb-2-trap-bar",
        }
    },
    {
        "slug": "titan-trap-bar",
        "name": "Titan Trap Bar",
        "category": "Specialty Bars",
        "description": "Closed-end hex bar. Affordable trap bar for deadlifts and shrugs.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/trap-bar",
            "rep_fitness": "https://repfitness.com/products/rep-trap-bar",
        }
    },
    {
        "slug": "swiss-bar-multi-grip",
        "name": "Multi-Grip Swiss Bar",
        "category": "Specialty Bars",
        "description": "Neutral grip pressing bar. Easier on shoulders than straight bar.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/multi-grip-swiss-bar",
            "rep_fitness": "https://repfitness.com/products/rep-multi-grip-bar",
        }
    },

    # ── BUMPER PLATES ─────────────────────────────────────────────────────────
    {
        "slug": "rogue-hg-2-bumper-plates",
        "name": "Rogue HG 2.0 Bumper Plates",
        "category": "Bumper Plates",
        "description": "Virgin rubber bumper plates. Sold in pairs.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-hg-2-0-bumper-plates",
        }
    },
    {
        "slug": "titan-competition-bumper-plates",
        "name": "Titan Competition Bumper Plates",
        "category": "Bumper Plates",
        "description": "Steel insert, low bounce competition-style bumpers.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/competition-bumper-plates",
        }
    },
    {
        "slug": "rep-fitness-bumper-plates",
        "name": "Rep Fitness Black Bumper Plates",
        "category": "Bumper Plates",
        "description": "Virgin rubber bumper plates with steel insert. Best value in class.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-black-bumper-plates",
        }
    },
    {
        "slug": "fringe-bumper-plates",
        "name": "FringeSport Bumper Plates",
        "category": "Bumper Plates",
        "description": "Color-coded virgin rubber bumpers. Sold in pairs.",
        "retailers": {
            "fringe": "https://www.fringesport.com/products/color-bumper-plates-by-fringesport",
        }
    },
    {
        "slug": "rep-fitness-color-bumper-plates",
        "name": "Rep Fitness Color Bumper Plates",
        "category": "Bumper Plates",
        "description": "IWF color-coded competition bumpers. Low bounce, steel insert.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-color-bumper-plates",
        }
    },

    # ── IRON PLATES ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-calibrated-plates",
        "name": "Rogue Calibrated Steel Plates",
        "category": "Iron Plates",
        "description": "Precision machined steel plates. IPF/IWF approved.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-calibrated-kt-plates",
        }
    },
    {
        "slug": "titan-iron-plates",
        "name": "Titan Cast Iron Plates",
        "category": "Iron Plates",
        "description": "Standard cast iron Olympic plates. Most affordable option.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/cast-iron-olympic-plates",
            "rep_fitness": "https://repfitness.com/products/rep-iron-plates",
        }
    },

    # ── POWER RACKS ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-rm-6",
        "name": "Rogue RM-6 Monster Rack",
        "category": "Power Racks",
        "description": "3x3 3/16\" monster rack. The most popular full-size home gym rack.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-rm-6-monster-rack",
        }
    },
    {
        "slug": "rogue-rml-390f",
        "name": "Rogue RML-390F Fold-Back Rack",
        "category": "Power Racks",
        "description": "Foldable wall-mount rack. Saves space without sacrificing strength.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rml-390f-fold-back-wall-mount-power-rack",
        }
    },
    {
        "slug": "titan-t-3-power-rack",
        "name": "Titan T-3 Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge steel. The most popular budget rack on the market.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/t-3-power-rack",
        }
    },
    {
        "slug": "titan-x-3-power-rack",
        "name": "Titan X-3 Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge steel. Titan's premium rack with more attachment options.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/x-3-flat-foot-power-rack",
        }
    },
    {
        "slug": "rep-fitness-pr-4000",
        "name": "Rep Fitness PR-4000 Power Rack",
        "category": "Power Racks",
        "description": "3x3 11-gauge modular rack. Tons of attachments available.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/pr-4000-power-rack",
        }
    },
    {
        "slug": "rep-fitness-pr-5000",
        "name": "Rep Fitness PR-5000 Power Rack",
        "category": "Power Racks",
        "description": "Rep's top-of-the-line rack. 1000lb rated, massive attachment ecosystem.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/pr-5000-power-rack",
        }
    },
    {
        "slug": "fringe-squat-stand",
        "name": "FringeSport Squat Stand",
        "category": "Power Racks",
        "description": "Budget squat stand for smaller spaces. No spotter arms included.",
        "retailers": {
            "fringe": "https://www.fringesport.com/products/squat-stand",
        }
    },

    # ── BENCHES ──────────────────────────────────────────────────────────────
    {
        "slug": "rogue-utility-bench-20",
        "name": "Rogue Utility Bench 2.0",
        "category": "Benches",
        "description": "Heavy-duty flat utility bench. 1000lb capacity.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-utility-bench-2-0",
        }
    },
    {
        "slug": "titan-competition-flat-bench",
        "name": "Titan Competition Flat Bench",
        "category": "Benches",
        "description": "IPF legal competition bench. 1200lb capacity.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/competition-flat-bench",
        }
    },
    {
        "slug": "rep-fitness-fb-5000",
        "name": "Rep Fitness FB-5000 Flat Bench",
        "category": "Benches",
        "description": "Commercial-grade flat bench. IPF competition spec.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-flat-bench-fb-5000",
        }
    },
    {
        "slug": "rep-fitness-ab-5200",
        "name": "Rep Fitness AB-5200 Adjustable Bench",
        "category": "Benches",
        "description": "7-position adjustable bench. Incline, flat, and decline.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-ab-5200-adjustable-bench",
        }
    },
    {
        "slug": "titan-adjustable-bench",
        "name": "Titan Adjustable Bench",
        "category": "Benches",
        "description": "Multi-angle adjustable bench. Budget-friendly incline option.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/adjustable-bench",
        }
    },

    # ── DUMBBELLS ────────────────────────────────────────────────────────────
    {
        "slug": "rogue-dumbbells",
        "name": "Rogue Rubber Hex Dumbbells",
        "category": "Dumbbells",
        "description": "Rubber-coated hex dumbbells. Sold individually or in sets.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-rubber-hex-dumbbells",
        }
    },
    {
        "slug": "rep-fitness-dumbbells",
        "name": "Rep Fitness Rubber Hex Dumbbells",
        "category": "Dumbbells",
        "description": "Rubber hex dumbbells with chrome handle. Best value per pound.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-rubber-hex-dumbbells",
        }
    },
    {
        "slug": "fringe-dumbbell-set",
        "name": "FringeSport Urethane Dumbbell Set",
        "category": "Dumbbells",
        "description": "Premium urethane coated dumbbells. Set of 5-50lb.",
        "retailers": {
            "fringe": "https://www.fringesport.com/products/urethane-dumbbells",
        }
    },

    # ── KETTLEBELLS ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-kettlebell",
        "name": "Rogue Powder Coat Kettlebell",
        "category": "Kettlebells",
        "description": "Single-piece cast iron, powder coated. Multiple weights.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-kettlebells",
        }
    },
    {
        "slug": "rep-fitness-kettlebell",
        "name": "Rep Fitness Cast Iron Kettlebell",
        "category": "Kettlebells",
        "description": "Single-piece cast iron, powder coated. Multiple weights.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-cast-iron-kettlebells",
        }
    },
    {
        "slug": "fringe-kettlebell",
        "name": "FringeSport Kettlebell",
        "category": "Kettlebells",
        "description": "Single cast iron kettlebell. Color-coded by weight.",
        "retailers": {
            "fringe": "https://www.fringesport.com/products/kettlebells-by-fringesport",
        }
    },

    # ── CARDIO ───────────────────────────────────────────────────────────────
    {
        "slug": "concept2-model-d-rower",
        "name": "Concept2 Model D Rowing Machine",
        "category": "Cardio",
        "description": "The gold standard rowing machine. Used in gyms and competitions worldwide.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/concept2-model-d-rower",
            "fringe": "https://www.fringesport.com/products/concept2-model-d-rower",
        }
    },
    {
        "slug": "assault-airbike",
        "name": "Assault AirBike Classic",
        "category": "Cardio",
        "description": "Fan bike with unlimited resistance. The most brutal cardio machine made.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/assault-airbike-classic",
        }
    },
    {
        "slug": "concept2-skierg",
        "name": "Concept2 SkiErg",
        "category": "Cardio",
        "description": "Ski-motion full body cardio. Great complement to the rower.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/concept2-skierg",
        }
    },
    {
        "slug": "echo-bike",
        "name": "Rogue Echo Bike",
        "category": "Cardio",
        "description": "Rogue's fan bike. Steel frame, all-metal construction, no electronics to break.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-echo-bike",
        }
    },

    # ── PULL-UP BARS ─────────────────────────────────────────────────────────
    {
        "slug": "rogue-monster-lite-pull-up-bar",
        "name": "Rogue Monster Lite Pull-Up System",
        "category": "Pull-Up Bars",
        "description": "Multi-grip pull-up bar for Monster Lite racks.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-monster-lite-pull-up-system",
        }
    },
    {
        "slug": "titan-multi-grip-pull-up-bar",
        "name": "Titan Multi-Grip Pull-Up Bar",
        "category": "Pull-Up Bars",
        "description": "Multiple grip positions, fits 2x2 and 3x3 uprights.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/multi-grip-pull-up-bar",
            "rep_fitness": "https://repfitness.com/products/rep-multi-grip-pull-up-bar",
        }
    },

    # ── GYM FLOORING ─────────────────────────────────────────────────────────
    {
        "slug": "rogue-horse-stall-mats",
        "name": "Rogue Horse Stall Mats",
        "category": "Gym Flooring",
        "description": "4x6 rubber stall mats. The most popular home gym flooring option.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-horse-stall-mats",
        }
    },
    {
        "slug": "rep-fitness-rubber-mats",
        "name": "Rep Fitness Rubber Floor Tiles",
        "category": "Gym Flooring",
        "description": "Interlocking rubber floor tiles. 3/8\" thick, sold per tile.",
        "retailers": {
            "rep_fitness": "https://repfitness.com/products/rep-rubber-floor-tiles",
        }
    },

    # ── ACCESSORIES ──────────────────────────────────────────────────────────
    {
        "slug": "rogue-wrist-wraps",
        "name": "Rogue Wrist Wraps",
        "category": "Accessories",
        "description": "24\" stiff wrist wraps. IPF approved for competition.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-wrist-wraps",
        }
    },
    {
        "slug": "rogue-knee-sleeves",
        "name": "Rogue Knee Sleeves",
        "category": "Accessories",
        "description": "7mm neoprene knee sleeves. Sold in pairs.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-knee-sleeves",
            "rep_fitness": "https://repfitness.com/products/rep-knee-sleeves",
        }
    },
    {
        "slug": "rogue-lifting-belt",
        "name": "Rogue Ohio Lifting Belt",
        "category": "Accessories",
        "description": "4\" leather lever belt. 10mm thick, IPF approved.",
        "retailers": {
            "rogue": "https://www.roguefitness.com/rogue-ohio-lifting-belt",
        }
    },
    {
        "slug": "titan-lever-belt",
        "name": "Titan Lever Belt",
        "category": "Accessories",
        "description": "10mm lever belt. IPF approved at a fraction of Rogue's price.",
        "retailers": {
            "titan": "https://www.titanfitness.com/products/lever-belt",
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
