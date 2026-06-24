from scraper.base import fetch, json_ld_price, og_price, extract_price


def scrape_price(url):
    soup = fetch(url)
    if not soup:
        return None, False

    # Rep Fitness runs on Shopify
    price = json_ld_price(soup)
    if price:
        return price, _check_in_stock(soup)

    price = og_price(soup)
    if price:
        return price, _check_in_stock(soup)

    for selector in [
        ".price__regular .price-item--regular",
        ".product__price",
        "[data-product-price]",
        ".product-single__price",
    ]:
        el = soup.select_one(selector)
        if el:
            price = extract_price(el.get_text())
            if price:
                return price, _check_in_stock(soup)

    return None, False


def _check_in_stock(soup):
    page_text = soup.get_text().lower()
    for signal in ["sold out", "out of stock", "unavailable"]:
        if signal in page_text:
            return False
    return True
