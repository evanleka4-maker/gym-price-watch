"""
Main entry point.
  python run.py          → start web server (scraper runs automatically every 24h)
  python run.py scrape   → run scraper once immediately, then exit
  python run.py seed     → seed the database with product catalog, then exit
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db import init_db
from database.seed import seed


def start_server():
    from apscheduler.schedulers.background import BackgroundScheduler
    from scraper.runner import run_all
    from web.app import app
    from config import SCRAPE_INTERVAL_HOURS

    init_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_all,
        trigger="interval",
        hours=SCRAPE_INTERVAL_HOURS,
        id="price_scraper",
        replace_existing=True,
    )
    scheduler.start()
    print(f"Scheduler running — prices will update every {SCRAPE_INTERVAL_HOURS}h.")

    try:
        port = int(os.environ.get("PORT", 5001))
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        scheduler.shutdown()


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "server"

    if command == "seed":
        init_db()
        seed()

    elif command == "scrape":
        init_db()
        from scraper.runner import run_all
        run_all()

    else:
        start_server()
