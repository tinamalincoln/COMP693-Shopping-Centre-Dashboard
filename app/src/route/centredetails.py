from flask import render_template, request, redirect, url_for, flash
from app import app, db
import os
from dotenv import load_dotenv
from datetime import datetime

from app.src.model.centres import (
    get_centre_by_osm, update_centre,
    set_image_filename, get_image_filename)
from app.src.model.geo import geocode_centremap, build_ors_reach_url
from app.src.model.image import save_or_replace_image, upload_dir

# Load ORS API key from .env
load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

# centredetails route to find a shopping centre by its OSM name
@app.route("/centredetails")
def centredetails():
    centre_name = request.args.get("name")
    if not centre_name:
        return render_template("centredetails.html", error="No shopping centre specified.")

    centre = get_centre_by_osm(centre_name)
    if not centre:
        return render_template("centredetails.html", error="Shopping centre not found.")

    lat, lon = geocode_centremap(centre)
    classic_map_url = build_ors_reach_url(lat, lon)

    return render_template(
        "centredetails.html",
        centre=centre,
        lat=lat,
        lon=lon,
        classic_map_url=classic_map_url,
        timestamp=datetime.now().timestamp()
    )

# Edit a shopping centre
@app.route("/edit/<int:centre_id>", methods=["POST"])
def edit_centre(centre_id):
    f = request.form
    image_file = request.files.get("image")

    # Normalize nullable fields (empty string -> None)
    fields = {
        "name": f.get("name", "").strip(),
        "osm_name": f.get("osm_name", "").strip(),
        "location": f.get("location", "").strip(),
        "date_opened": f.get("date_opened") or None,
        "site_area_ha": f.get("site_area_ha") or None,
        "covered_parking_num": f.get("covered_parking_num") or None,
        "uncovered_parking_num": f.get("uncovered_parking_num") or None,
        "redevelopments": f.get("redevelopments") or None,
        "levels": (f.get("levels") or None),
        "total_retail_space": f.get("total_retail_space") or None,
    }

    # Update DB fields first
    update_centre(centre_id, fields)

    # If a new image is uploaded, delete old image on disk manually, then save new
    if image_file and image_file.filename:
        # Ensure upload folder exists
        folder = upload_dir()
        os.makedirs(folder, exist_ok=True)

        # Fetch current filename
        old_filename = get_image_filename(centre_id)

        # Delete old file if present
        if old_filename:
            old_path = os.path.join(folder, old_filename)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete old image {old_path}: {e}")

        # Save new file using your existing 3-arg helper
        try:
            new_filename = save_or_replace_image(centre_id, fields["name"], image_file)  # 3 args
            if new_filename:
                set_image_filename(centre_id, new_filename)
        except ValueError as ve:
            # e.g., unsupported file type
            flash(str(ve), "warning")

    # Commit any pending changes
    db.get_db().commit()

    flash("Centre updated successfully.", "success")
    return redirect(url_for("centredetails", name=fields["osm_name"]))

# Delete a shopping centre
@app.route("/delete/<int:centre_id>", methods=["POST"])
def delete_centre(centre_id):
    folder = upload_dir()

    with db.get_cursor() as cursor:
        # Get everything we need *including city* BEFORE deleting
        cursor.execute("""
            SELECT sc.name, sc.osm_name, sc.image_filename, ci.name AS city_name
            FROM shopping_centre sc
            JOIN city ci ON ci.id = sc.city_id
            WHERE sc.id = %s
        """, (centre_id,))
        centre = cursor.fetchone()

        if not centre:
            flash("Centre not found.", "danger")
            return redirect(url_for("city_summary"))

        city_name = centre["city_name"]
        centre_name = centre["name"]

        # Delete photo if present
        img = centre.get("image_filename")
        if img:
            old_path = os.path.join(folder, img)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete image file {old_path}: {e}")

        # Delete DB row
        cursor.execute("DELETE FROM shopping_centre WHERE id = %s", (centre_id,))

    db.get_db().commit()

    # Inform the user and go back to this city's list
    flash(f"Deleted ‘{centre_name}’ in {city_name}.", "success")
    return redirect(url_for("centrelist", city=city_name))
