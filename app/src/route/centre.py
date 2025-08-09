from flask import render_template, request, redirect, url_for, flash
from app import app, db
import os
from dotenv import load_dotenv
from datetime import datetime

from app.src.model.centre import get_centre_by_osm
from app.src.model.image import upload_dir, save_or_replace_image  
from app.src.model.geo import geocode_if_needed, build_ors_reach_url

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

# search route to find a shopping centre by its OSM name
@app.route("/search")
def search():
    centre_name = request.args.get("name")
    if not centre_name:
        return render_template("search.html", error="No shopping centre specified.")

    centre = get_centre_by_osm(centre_name)
    if not centre:
        return render_template("search.html", error="Shopping centre not found.")

    lat, lon = geocode_if_needed(centre)
    classic_map_url = build_ors_reach_url(lat, lon)

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
    f = request.form
    image_file = request.files.get("image")

    # convert empties to None for nullable columns
    date_opened = f["date_opened"] or None
    site_area_ha = f["site_area_ha"] or None
    covered_parking = f["covered_parking_num"] or None
    uncovered_parking = f["uncovered_parking_num"] or None
    redevelopments = f["redevelopments"] or None
    levels = f["levels"] or None
    total_space = f["total_retail_space"] or None

    with db.get_cursor() as cursor:
        cursor.execute("""
            UPDATE shopping_centre
            SET name=%s, osm_name=%s, location=%s, date_opened=%s, site_area_ha=%s,
                covered_parking_num=%s, uncovered_parking_num=%s, redevelopments=%s,
                levels=%s, total_retail_space=%s
            WHERE id=%s
        """, (
            f["name"], f["osm_name"], f["location"], date_opened, site_area_ha,
            covered_parking, uncovered_parking, redevelopments, levels, total_space, centre_id
        ))

        # image handling
        try:
            new_filename = save_or_replace_image(centre_id, f["name"], image_file)
            if new_filename:
                cursor.execute(
                    "UPDATE shopping_centre SET image_filename=%s WHERE id=%s",
                    (new_filename, centre_id)
                )
        except ValueError as ve:
            flash(str(ve), "warning")

    db.get_db().commit()
    flash("Centre updated successfully.", "success")
    return redirect(url_for("search", name=f["osm_name"]))


# Delete a shopping centre
@app.route("/delete/<int:centre_id>", methods=["POST"])
def delete_centre(centre_id):
    folder = upload_dir()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT name, osm_name, image_filename FROM shopping_centre WHERE id=%s", (centre_id,))
        centre = cursor.fetchone()
        if not centre:
            flash("Centre not found.", "danger")
            return redirect(url_for("home"))

        img = centre.get("image_filename")
        if img:
            old_path = os.path.join(folder, img)
            if os.path.isfile(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete image file {old_path}: {e}")

        cursor.execute("DELETE FROM shopping_centre WHERE id=%s", (centre_id,))

    db.get_db().commit()
    flash(f"Deleted centre: {centre['name']}", "success")
    return redirect(url_for("home"))
