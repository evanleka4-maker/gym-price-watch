from scraper.base import fetch, json_ld_price, og_price, extract_price


def scrape_price(url):
    soup = fetch(url)
    if not soup:
        return None, False

    # 1. JSON-LD structured data (most reliable)
    price = json_ld_price(soup)
    if price:
        return price, _check_in_stock(soup)

    # 2. Open Graph price tag
    price = og_price(soup)
    if price:
        return price, _check_in_stock(soup)

    # 3. Rogue-specific price elements
    for selector in [
        ".price-display",
        ".product-price",
        "[data-price]",
        ".final-price",
    ]:
        el = soup.select_one(selector)
        if el:
            price = extract_price(el.get_text())
            if price:
                return price, _check_in_stock(soup)

    return None, False


def _check_in_stock(soup):
    out_of_stock_signals = [
        "out of stock",
        "sold out",
        "unavailable",
        "notify me",
    ]
    page_text = soup.get_text().lower()
    for signal in out_of_stock_signals:
        if signal in page_text:
            return False
    return True
