import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, redirect
from database.db import (
    get_all_categories, get_products_by_category,
    get_product_by_slug, search_products, get_best_deals,
    save_subscriber
)
from config import SITE_NAME, SITE_TAGLINE

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.context_processor
def inject_globals():
    return {
        "site_name": SITE_NAME,
        "categories": get_all_categories(),
    }


@app.route("/sitemap.xml")
def sitemap():
    from flask import Response
    from database.db import get_conn
    base = "https://web-production-76350.up.railway.app"
    conn = get_conn()
    products = conn.execute("SELECT slug FROM products").fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM products").fetchall()
    conn.close()

    urls = [base + "/"]
    for c in categories:
        urls.append(f"{base}/category/{c['category']}")
    for p in products:
        urls.append(f"{base}/product/{p['slug']}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"  <url><loc>{url}</loc></url>\n"
    xml += "</urlset>"
    return Response(xml, mimetype="application/xml")


@app.route("/googleaabca5936e2a4a7d.html")
def google_verify():
    return "google-site-verification: googleaabca5936e2a4a7d.html"


@app.route("/")
def index():
    deals = get_best_deals(limit=6)
    categories = get_all_categories()
    return render_template("index.html", deals=deals, tagline=SITE_TAGLINE, categories=categories)


@app.route("/category/<category>")
def category(category):
    products = get_products_by_category(category)
    return render_template("category.html", category=category, products=products)


@app.route("/product/<slug>")
def product(slug):
    data = get_product_by_slug(slug)
    if not data:
        return "Product not found", 404

    # Build chart data grouped by retailer
    history = data["history"]
    retailers = list({h["retailer"] for h in history})
    chart_labels = sorted(list({h["scraped_at"][:10] for h in history}))
    chart_datasets = []
    colors = {
        "rogue": "#e63946",
        "titan": "#457b9d",
        "rep_fitness": "#2a9d8f",
        "amazon": "#f4a261",
    }
    for retailer in retailers:
        prices_by_date = {h["scraped_at"][:10]: h["price"]
                         for h in history if h["retailer"] == retailer}
        data_points = [prices_by_date.get(d) for d in chart_labels]
        chart_datasets.append({
            "label": retailer.replace("_", " ").title(),
            "data": data_points,
            "borderColor": colors.get(retailer, "#888"),
            "backgroundColor": "transparent",
            "tension": 0.3,
        })

    return render_template(
        "product.html",
        product=data["product"],
        listings=data["listings"],
        chart_labels=chart_labels,
        chart_datasets=chart_datasets,
    )


@app.route("/subscribe", methods=["POST"])
def subscribe():
    email = request.form.get("email", "").strip()
    product = request.form.get("product", "").strip()
    if email:
        save_subscriber(email, product)
        from web.emailer import notify_new_subscriber
        notify_new_subscriber(email, product)
    return redirect(request.referrer or "/")


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = search_products(q) if q else []
    return render_template("search.html", query=q, results=results)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
