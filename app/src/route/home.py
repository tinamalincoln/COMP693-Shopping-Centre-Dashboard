from flask import render_template, request, redirect, url_for, flash
from app import app, db
import requests
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from datetime import datetime

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

@app.route("/")
def home():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                sc.id, sc.name, sc.osm_name, sc.location,
                c.name AS classification, t.name AS centre_type
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            ORDER BY sc.name ASC
        """)
        centres = cursor.fetchall()

    default_lat, default_lon = -43.5321, 172.6362
    return render_template("home.html", centres=centres, lat=default_lat, lon=default_lon)


@app.route("/search")
def search():
    centre_name = request.args.get("name")

    if not centre_name:
        return render_template("search.html", error="No shopping centre specified.")

    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                sc.id, sc.name, sc.osm_name, sc.image_filename, sc.location, sc.total_retail_space, sc.date_opened, sc.site_area_ha, 
                sc.covered_parking_num, sc.uncovered_parking_num, sc.redevelopments, sc.levels,
                c.name AS classification, t.name AS centre_type, ci.name AS city_name
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            LEFT JOIN city ci ON sc.city_id = ci.id
            WHERE sc.osm_name = %s
        """, (centre_name,))
        centre = cursor.fetchone()

    if not centre:
        return render_template("search.html", error="Shopping centre not found.")
    
    query = centre['osm_name']
    city_name = centre['city_name']
    
    # Handle special case where the centre is outside Christchurch
    
    if query == "Woolworths, 121 Carters Road":
        location_query = query + ", Amberley, New Zealand"
    elif query == "Rolleston Square":
        location_query = query + ", Rolleston, New Zealand"
    elif city_name:
        location_query = query + ", " + city_name + ", New Zealand"
    else:
        location_query = query + ", Christchurch, New Zealand"
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location_query,
        "format": "json",
        "limit": 1
    }


    response = requests.get(url, headers={"User-Agent": "shopping-centre-dashboard"}, params=params)

    if response.status_code == 200 and response.json():
        location = response.json()[0]
        lat, lon = float(location["lat"]), float(location["lon"])
    else:
        lat, lon = -43.5321, 172.6362

    classic_map_url = f"https://classic-maps.openrouteservice.org/reach?n1={lat}&n2={lon}&n3=15&a={lat},{lon}&b=0&i=0&j1=10&j2=2&k1=en-US&k2=km"

    return render_template(
        "search.html",
        centre=centre,
        lat=lat,
        lon=lon,
        classic_map_url=classic_map_url,
        timestamp=datetime.now().timestamp()
    )


# Edit a shopping centre
@app.route("/edit/<int:centre_id>", methods=["POST"])
def edit_centre(centre_id):
    form = request.form
    image_file = request.files.get("image")

    # Convert empty fields to None
    date_opened = form["date_opened"] or None
    site_area_ha = form["site_area_ha"] or None
    covered_parking = form["covered_parking_num"] or None
    uncovered_parking = form["uncovered_parking_num"] or None
    redevelopments = form["redevelopments"] or None
    levels = form["levels"] or None
    total_space = form["total_retail_space"] or None


    # Always resolve full path from app root
    upload_folder = os.path.join(app.root_path, "static", "uploads", "centre_photo")
    os.makedirs(upload_folder, exist_ok=True)

    with db.get_cursor() as cursor:
        # Update centre fields
        cursor.execute("""
            UPDATE shopping_centre
            SET name=%s, osm_name=%s, location=%s, date_opened=%s, site_area_ha=%s,
                covered_parking_num=%s, uncovered_parking_num=%s, redevelopments=%s,
                levels=%s, total_retail_space=%s
            WHERE id=%s
        """, (
            form["name"], form["osm_name"], form["location"], date_opened, site_area_ha,
            covered_parking, uncovered_parking, redevelopments, levels, total_space, centre_id
        ))

        if image_file and image_file.filename != "":
            # Construct new filename
            filename = secure_filename(image_file.filename)
            ext = filename.rsplit(".", 1)[-1].lower()
            new_filename = f"{form['name'].replace(' ', '')}_{centre_id}.{ext}"
            new_image_path = os.path.join(upload_folder, new_filename)

            # Delete old image if different
            cursor.execute("SELECT image_filename FROM shopping_centre WHERE id = %s", (centre_id,))
            result = cursor.fetchone()
            old_filename = result.get("image_filename") if result else None
            if old_filename and old_filename != new_filename:
                old_image_path = os.path.join(upload_folder, old_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            # Save new image
            image_file.save(new_image_path)

            # Update DB with new filename
            cursor.execute("UPDATE shopping_centre SET image_filename=%s WHERE id=%s",
                           (new_filename, centre_id))

    db.get_db().commit()
    flash("Centre updated successfully.", "success")
    return redirect(url_for("search", name=form["osm_name"]))



# Delete a shopping centre
@app.route("/delete/<int:centre_id>", methods=["POST"])
def delete_centre(centre_id):
    # Resolve your upload folder safely (so we don’t create a rogue /static)
    upload_folder = os.path.join(app.root_path, "static", "uploads", "centre_photo")

    with db.get_cursor() as cursor:
        # Grab what we need before deleting (image + name for message)
        cursor.execute("""
            SELECT name, osm_name, image_filename
            FROM shopping_centre
            WHERE id = %s
        """, (centre_id,))
        centre = cursor.fetchone()

        if not centre:
            flash("Centre not found.", "danger")
            return redirect(url_for("home"))

        # Delete image on disk if present
        img = centre.get("image_filename")
        if img:
            old_path = os.path.join(upload_folder, img)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete image file {old_path}: {e}")

        # Delete the row
        cursor.execute("DELETE FROM shopping_centre WHERE id = %s", (centre_id,))

    db.get_db().commit()
    flash(f"Deleted centre: {centre['name']}", "success")
    return redirect(url_for("home"))
