from scraper.base import fetch, json_ld_price, og_price, extract_price


def scrape_price(url):
    soup = fetch(url)
    if not soup:
        return None, False

    # Titan runs on Shopify — JSON-LD is very reliable here
    price = json_ld_price(soup)
    if price:
        return price, _check_in_stock(soup)

    price = og_price(soup)
    if price:
        return price, _check_in_stock(soup)

    # Shopify standard price selectors
    for selector in [
        ".price__regular .price-item--regular",
        ".product__price .price",
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
    sold_out = soup.find(class_=lambda c: c and "sold-out" in c)
    if sold_out:
        return False
    page_text = soup.get_text().lower()
    for signal in ["sold out", "out of stock", "unavailable"]:
        if signal in page_text:
            return False
    return True
