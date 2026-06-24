import json as _json
from scraper.base import _http, HEADERS
import urllib3


def scrape_price(url):
    # FringeSport Shopify store — use the product JSON endpoint for reliable price extraction
    json_url = url.rstrip('/') + '.json'
    try:
        resp = _http.request('GET', json_url, headers=HEADERS,
                             timeout=urllib3.Timeout(connect=8, read=20))
        if resp.status >= 400:
            print(f"  [FAIL] {json_url} — {resp.status}")
            return None, False
        data = _json.loads(resp.data.decode('utf-8'))
        variants = data.get('product', {}).get('variants', [])
        if not variants:
            return None, False
        price = float(variants[0]['price'])
        available = variants[0].get('available', True)
        return price, available
    except Exception as e:
        print(f"  [FAIL] {json_url} — {e}")
        return None, False
