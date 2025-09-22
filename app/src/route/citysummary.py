# app/src/route/citysummary.py
from flask import render_template, url_for, request, flash, redirect
from app import app, db
import math
import os
from werkzeug.utils import secure_filename

# City summary route
@app.route("/")
@app.route("/city-summary")
def city_summary():
    # Read & sanitise query params
    q = request.args.get("q", "").strip()
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 8))
    
    # Load cities with optional search + pagination
    with db.get_cursor() as cursor:
        if q:
            cursor.execute("""
                SELECT ci.id,
                       ci.name AS city_name,
                       ci.image_filename,
                       COUNT(sc.id) AS mall_count
                FROM city ci
                LEFT JOIN shopping_centre sc ON sc.city_id = ci.id
                WHERE ci.name LIKE %s
                GROUP BY ci.id
                ORDER BY ci.name ASC
                LIMIT %s OFFSET %s
            """, (f"%{q}%", per_page, (page - 1) * per_page))
        else:
            cursor.execute("""
                SELECT ci.id,
                       ci.name AS city_name,
                       ci.image_filename,
                       COUNT(sc.id) AS mall_count
                FROM city ci
                LEFT JOIN shopping_centre sc ON sc.city_id = ci.id
                GROUP BY ci.id
                ORDER BY ci.name ASC
                LIMIT %s OFFSET %s
            """, (per_page, (page - 1) * per_page))

        rows = cursor.fetchall()

        # Get total count for pagination
        cursor.execute("SELECT COUNT(*) AS total FROM city")
        total = cursor.fetchone()["total"]

    total_pages = (total + per_page - 1) // per_page

    # Build cities list with safe URLs
    cities = []
    for r in rows:
        if r["image_filename"]:
            image_url = url_for("static", filename=f"uploads/city_photo/{r['image_filename']}")
        else:
            image_url = url_for("static", filename="images/default_city.jpg")

        r["image_url"] = image_url
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

# Delete a city (and its centres if any)
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


# Helper: resolve upload folder for city images
def city_upload_dir():
    folder = os.path.join(app.root_path, "static", "uploads", "city_photo")
    os.makedirs(folder, exist_ok=True)
    return folder

# Edit a city (name + image)
@app.route("/edit_city/<int:city_id>", methods=["POST"])
def edit_city(city_id):
    form = request.form
    new_name = form.get("city_name").strip()
    image_file = request.files.get("image")
    
    # Validate
    upload_folder = os.path.join(app.root_path, "static", "uploads", "city_photo")
    os.makedirs(upload_folder, exist_ok=True)

    with db.get_cursor() as cursor:
        # Fetch old data (for current image filename)
        cursor.execute("SELECT name, image_filename FROM city WHERE id = %s", (city_id,))
        city = cursor.fetchone()
        if not city:
            flash("City not found.", "danger")
            return redirect(url_for("city_summary"))

        # Update name
        cursor.execute("UPDATE city SET name=%s WHERE id=%s", (new_name, city_id))

        # If image uploaded
        if image_file and image_file.filename:
            ext = secure_filename(image_file.filename).rsplit(".", 1)[-1].lower()
            # Always use new city name (no spaces)
            new_filename = f"{new_name.replace(' ', '')}.{ext}"
            new_path = os.path.join(upload_folder, new_filename)

            # Remove old image if different
            old_filename = city.get("image_filename")
            if old_filename and old_filename != new_filename:
                old_path = os.path.join(upload_folder, old_filename)
                if os.path.exists(old_path):
                    try:
                        os.remove(old_path)
                    except Exception as e:
                        app.logger.warning(f"Could not remove old city image {old_path}: {e}")

            # Save new file
            image_file.save(new_path)

            # Update DB reference
            cursor.execute("UPDATE city SET image_filename=%s WHERE id=%s", (new_filename, city_id))

    db.get_db().commit()
    flash(f'City "{new_name}" updated successfully.', "success")
    return redirect(url_for("city_summary"))
