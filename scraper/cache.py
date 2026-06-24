import threading
from datetime import datetime

_lock = threading.Lock()
_prices = {}  # {listing_id: {price, in_stock, scraped_at}}


def set_price(listing_id, price, in_stock):
    with _lock:
        _prices[listing_id] = {
            "price": price,
            "in_stock": in_stock,
            "scraped_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M"),
        }


def get_price(listing_id):
    with _lock:
        return _prices.get(listing_id, {"price": None, "in_stock": None, "scraped_at": None})


def all_prices():
    with _lock:
        return dict(_prices)
