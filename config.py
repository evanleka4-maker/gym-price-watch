import os
from dotenv import load_dotenv

load_dotenv()

# --- Affiliate IDs (fill these in after signing up) ---
# Rogue: https://www.roguefitness.com/affiliates
# Titan: https://www.titanfitness.com/pages/affiliates
# Rep: https://repfitness.com/pages/affiliate-program
# Amazon: https://affiliate-program.amazon.com

AFFILIATE_IDS = {
    "rogue": os.getenv("ROGUE_AFFILIATE_ID", "YOUR_ROGUE_ID"),
    "titan": os.getenv("TITAN_AFFILIATE_ID", "YOUR_TITAN_ID"),
    "rep_fitness": os.getenv("REP_AFFILIATE_ID", "YOUR_REP_ID"),
    "amazon": os.getenv("AMAZON_ASSOCIATE_ID", "YOUR_AMAZON_TAG-20"),
}

DATABASE_PATH = os.getenv("DATABASE_PATH", "gym_prices.db")
SCRAPE_INTERVAL_HOURS = int(os.getenv("SCRAPE_INTERVAL_HOURS", "24"))
SITE_NAME = "GymPriceWatch"
SITE_TAGLINE = "Find the best price on gym equipment — updated daily"
