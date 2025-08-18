# app/src/route/citysummary.py
from flask import render_template, url_for
from app import app, db

def city_image_filename(city_name: str) -> str:
    # Simple slug -> "Christchurch" -> "Christchurch.jpg"
    # Replace spaces with underscores to match your file naming convention
    safe = city_name.replace(" ", "_")
    return f"uploads/city_photo/{safe}.jpg"

@app.route("/")
@app.route("/city-summary")
def city_summary():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT ci.name AS city_name, COUNT(sc.id) AS mall_count
            FROM city ci
            LEFT JOIN shopping_centre sc ON sc.city_id = ci.id
            GROUP BY ci.id, ci.name
            ORDER BY ci.name ASC
        """)
        rows = cursor.fetchall()

    # Enrich with image URL (no DB change required)
    cities = []
    for r in rows:
        img_rel = city_image_filename(r["city_name"])
        r["image_url"] = url_for("static", filename=img_rel)
        r["fallback_url"] = url_for("static", filename="images/default_city.jpg")
        cities.append(r)

    return render_template("citysummary.html", cities=cities)
