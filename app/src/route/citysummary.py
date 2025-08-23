# app/src/route/citysummary.py
from flask import render_template, url_for, request, flash, redirect
from app import app, db
import math

def city_image_filename(city_name: str) -> str:
    # Simple slug -> "Christchurch" -> "Christchurch.jpg"
    # Replace spaces with underscores to match your file naming convention
    safe = city_name.replace(" ", "_")
    return f"uploads/city_photo/{safe}.jpg"

@app.route("/")
@app.route("/city-summary")
def city_summary():
    
# Read & sanitise query params
    q = request.args.get("q", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 4))

    
    with db.get_cursor() as cursor:
        if q:
            cursor.execute("""
                SELECT ci.id, ci.name AS city_name, COUNT(sc.id) AS mall_count
                FROM city ci
                LEFT JOIN shopping_centre sc ON sc.city_id = ci.id
                WHERE ci.name LIKE %s
                GROUP BY ci.id
                ORDER BY ci.name ASC
                LIMIT %s OFFSET %s
            """, (f"%{q}%", per_page, (page-1)*per_page))
        else:
            cursor.execute("""
                SELECT ci.id, ci.name AS city_name, COUNT(sc.id) AS mall_count
                FROM city ci
                LEFT JOIN shopping_centre sc ON sc.city_id = ci.id
                GROUP BY ci.id
                ORDER BY ci.name ASC
                LIMIT %s OFFSET %s
            """, (per_page, (page-1)*per_page))

        rows = cursor.fetchall()

        # Get total for pagination
        cursor.execute("SELECT COUNT(*) AS total FROM city")
        total = cursor.fetchone()["total"]

    total_pages = (total + per_page - 1) // per_page

   
   
    # Enrich with image URL (no DB change required)
    cities = []
    for r in rows:
        img_rel = city_image_filename(r["city_name"])
        r["image_url"] = url_for("static", filename=img_rel)
        r["fallback_url"] = url_for("static", filename="images/default_city.jpg")
        cities.append(r)

    return render_template(
        "citysummary.html",
        cities=cities,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
    )

@app.route("/delete_city/<int:city_id>", methods=["POST"])
def delete_city(city_id):
    with db.get_cursor() as cursor:
        cursor.execute("SELECT name FROM city WHERE id=%s", (city_id,))
        city = cursor.fetchone()
        if not city:
            flash("City not found.", "danger")
            return redirect(url_for("city_summary"))

        # If you don't have ON DELETE CASCADE, delete centres first:
        cursor.execute("DELETE FROM shopping_centre WHERE city_id=%s", (city_id,))
        cursor.execute("DELETE FROM city WHERE id=%s", (city_id,))

    db.get_db().commit()
    flash(f"Deleted city: {city['name']}", "success")
    return redirect(url_for("city_summary"))

