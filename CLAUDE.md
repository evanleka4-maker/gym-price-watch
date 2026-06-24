# GymPriceWatch

Affiliate price comparison site for gym equipment. Tracks prices daily across Rogue, Titan, Rep Fitness, and FringeSport. Earns Amazon Associates commissions on purchases.

## Live Site
https://web-production-76350.up.railway.app

## Stack
- **Backend:** Python / Flask
- **Database:** SQLite (product catalog only — seeded on every startup)
- **Prices:** In-memory cache (`scraper/cache.py`) — scraped on startup, refreshed every 24h
- **Scraping:** BeautifulSoup + requests, JSON-LD structured data extraction
- **Scheduler:** APScheduler background jobs
- **Hosting:** Railway (auto-deploys from GitHub on push)
- **Repo:** https://github.com/evanleka4-maker/gym-price-watch

## Key Architecture Decision
Prices are NOT stored in the database — they live in memory only. This is intentional: Railway has an ephemeral filesystem so SQLite prices got wiped on every redeploy. The product catalog (slugs, names, retailer URLs) is stored in SQLite and re-seeded on every startup from `database/seed.py`.

## Commands
```bash
python3 run.py          # start server (seeds + scrapes on startup, port 5001 locally)
python3 run.py seed     # seed product catalog only
python3 run.py scrape   # run scraper once and exit
```

## Project Structure
```
run.py                  # entry point — seeds, starts scheduler, starts Flask
config.py               # affiliate IDs loaded from env vars
database/
  db.py                 # all DB queries + affiliate URL generation
  seed.py               # product catalog (62 products, 12 categories)
  add_amazon.py         # one-time script to add Amazon listings
scraper/
  cache.py              # thread-safe in-memory price store
  runner.py             # runs all scrapers, writes to cache
  base.py               # shared fetch() + price extraction helpers
  rogue.py              # Rogue Fitness scraper
  titan.py              # Titan Fitness scraper (Shopify)
  rep_fitness.py        # Rep Fitness scraper (Shopify)
  fringe.py             # FringeSport scraper (Shopify)
web/
  app.py                # Flask routes
  templates/            # Jinja2 HTML templates
  static/css/style.css  # Bootstrap 5 + custom styles
```

## Retailers + Affiliate Programs
| Retailer | Affiliate Program | Status |
|----------|------------------|--------|
| Amazon | Associates (`gympricewatch-20`) | Active |
| Rogue | Impact | Not signed up yet |
| Titan | Their own program | Not signed up yet |
| Rep Fitness | Their own program | Not signed up yet |
| FringeSport | Their own program | Not signed up yet |

## Environment Variables (set in Railway)
```
AMAZON_ASSOCIATE_ID=gympricewatch-20
ROGUE_AFFILIATE_ID=
TITAN_AFFILIATE_ID=
REP_AFFILIATE_ID=
FRINGE_AFFILIATE_ID=
SCRAPE_INTERVAL_HOURS=24
```

## Catalog Structure
Products come in two types:
1. **Brand-specific** — e.g. "Rogue Ohio Bar" (one retailer)
2. **Comparison pages** — e.g. "Men's Olympic Barbell — Price Comparison" (3-4 retailers, these are the hero pages)

Comparison page slugs start with `compare-`. These are the most valuable SEO pages.

## Known Issues / TODO
- Scrapers hang on macOS due to LibreSSL — work fine on Railway (Linux/OpenSSL)
- Price drop alert form uses Formspree endpoint `xpwzgdjv` — needs real Formspree account
- Amazon ASINs in `add_amazon.py` should be verified for accuracy
- Need to sign up for Rogue/Titan/Rep/Fringe affiliate programs to earn on non-Amazon clicks
- Price history charts are disabled (no persistent storage) — could re-enable with Railway Volume or Supabase

## Traffic Strategy
- Facebook home gym groups (posted, waiting for responses)
- Google Search Console verified, sitemap submitted
- Reddit r/homegym — build karma first, then post
- SEO: 62 product pages + 12 category pages indexed
