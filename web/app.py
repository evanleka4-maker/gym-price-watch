import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, Response
from database.db import (
    get_all_categories, get_products_by_category,
    get_product_by_slug, search_products, get_best_deals,
    get_all_products_with_prices
)
from config import SITE_NAME, SITE_TAGLINE

app = Flask(__name__, template_folder="templates", static_folder="static")

CATEGORY_GUIDES = {
    "Barbells": {
        "intro": "A good barbell is the single most important piece of equipment in any home gym. Prices vary significantly across retailers — sometimes by $100 or more for the same quality of bar. We track prices daily so you always know where to get the best deal.",
        "tips": [
            "For most lifters, a 20kg multipurpose bar in the $200-300 range is the sweet spot.",
            "Power bars (29mm) are stiffer and better for squats and deadlifts. Olympic bars (28mm) have more whip for cleans and snatches.",
            "Tensile strength matters: 190k PSI is good, 210k+ is excellent.",
            "Rogue's Ohio Bar is the benchmark. Titan and Rep Fitness offer similar quality for less.",
        ]
    },
    "Power Racks": {
        "intro": "A power rack is the foundation of a home gym. The price gap between Rogue and budget alternatives can be $500+. All of the racks we track are 3x3 11-gauge steel — the difference is mostly branding and attachment ecosystems.",
        "tips": [
            "3x3 11-gauge steel is the minimum standard for a serious home gym rack.",
            "Titan's T-3 is the most popular budget rack. Rogue's Monster series is the gold standard.",
            "Consider the attachment ecosystem — Rep Fitness and Titan have extensive, affordable accessories.",
            "Foldable wall-mount racks save floor space but require solid wall studs.",
        ]
    },
    "Bumper Plates": {
        "intro": "Bumper plate prices are the most volatile of any gym equipment — they swing $50-100 per pair during sales events. Tracking prices daily across retailers is the easiest way to save money on a full plate set.",
        "tips": [
            "Virgin rubber bumpers are more durable than recycled rubber. All plates we track are virgin rubber.",
            "Buy in sets if you can — per-pound prices drop significantly at higher quantities.",
            "Rogue plates are premium but rarely the cheapest. Rep Fitness and Titan offer nearly identical quality.",
            "45lb pairs are the most common purchase — we track those specifically.",
        ]
    },
    "Benches": {
        "intro": "A quality flat bench doesn't need to cost $500. Titan and Rep Fitness both make IPF-spec benches that are nearly indistinguishable from Rogue's at a fraction of the price.",
        "tips": [
            "For powerlifting, look for IPF legal specs: 12\" width, flat surface, specific height range.",
            "Adjustable benches add versatility but add instability at heavy weights.",
            "1000lb+ capacity rating is standard for serious training benches.",
            "Rep Fitness FB-5000 and Titan's competition bench are the most recommended budget options.",
        ]
    },
    "Cardio": {
        "intro": "Cardio equipment for home gyms has a clear tier list. The Concept2 rower and Echo Bike sit at the top — both are virtually indestructible and used in commercial gyms worldwide. Prices are relatively stable but vary by retailer.",
        "tips": [
            "The Concept2 Model D is the most resold piece of gym equipment — holds value extremely well.",
            "Fan bikes (Echo Bike, Assault Bike) provide unlimited resistance and never wear out.",
            "Check multiple retailers — the same Concept2 rower can vary by $50-100 across sites.",
            "All cardio equipment we track ships free from most retailers.",
        ]
    },
    "Specialty Bars": {
        "intro": "Specialty bars like safety squat bars and trap bars can transform your training. Prices vary significantly — Rogue's SSB costs nearly twice what Titan's does for similar performance.",
        "tips": [
            "Safety squat bars reduce shoulder strain and allow squatting with upper body injuries.",
            "Trap bars are excellent for deadlift variations and are more beginner-friendly than straight bars.",
            "Swiss bars allow neutral grip pressing — easier on shoulder joints for most lifters.",
            "Titan and Rep Fitness offer specialty bars at 40-50% less than Rogue.",
        ]
    },
}


@app.context_processor
def inject_globals():
    return {
        "site_name": SITE_NAME,
        "categories": get_all_categories(),
    }


@app.route("/sitemap.xml")
def sitemap():
    from database.db import get_conn
    base = "https://web-production-76350.up.railway.app"
    conn = get_conn()
    products = conn.execute("SELECT slug FROM products").fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM products").fetchall()
    conn.close()

    urls = [base + "/", base + "/deals"]
    for c in categories:
        urls.append(f"{base}/category/{c['category']}")
        urls.append(f"{base}/guide/{c['category'].lower().replace(' ', '-')}")
    for p in products:
        urls.append(f"{base}/product/{p['slug']}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"  <url><loc>{url}</loc><changefreq>daily</changefreq></url>\n"
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


@app.route("/deals")
def deals():
    all_deals = get_best_deals(limit=50)
    return render_template("deals.html", deals=all_deals)


@app.route("/guide/<slug>")
def guide(slug):
    category = slug.replace("-", " ").title()
    products = get_products_by_category(category)
    guide_content = CATEGORY_GUIDES.get(category, {})
    if not products:
        return "Guide not found", 404
    return render_template("guide.html", category=category,
                           products=products, guide=guide_content)


@app.route("/category/<category>")
def category(category):
    products = get_products_by_category(category)
    return render_template("category.html", category=category, products=products)


@app.route("/product/<slug>")
def product(slug):
    data = get_product_by_slug(slug)
    if not data:
        return "Product not found", 404
    return render_template(
        "product.html",
        product=data["product"],
        listings=data["listings"],
        chart_labels=[],
        chart_datasets=[],
    )


@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    results = search_products(q) if q else []
    return render_template("search.html", query=q, results=results)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
