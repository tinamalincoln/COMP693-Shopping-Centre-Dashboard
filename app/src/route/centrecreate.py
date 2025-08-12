from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.src.model.image import upload_dir, save_or_replace_image
import os

# GET: show the blank form
@app.route("/centres/new", methods=["GET"])
def new_centre():
    # Load dropdowns
    with db.get_cursor() as cur:
        cur.execute("SELECT id, name FROM city ORDER BY name")
        cities = cur.fetchall()
        cur.execute("SELECT id, name FROM classification ORDER BY name")
        classes = cur.fetchall()
        cur.execute("SELECT id, name FROM centre_type ORDER BY name")
        types = cur.fetchall()

    return render_template("centrenew.html", cities=cities, classes=classes, types=types)

# POST: create the row (and image if provided)
@app.route("/centres/new", methods=["POST"])
def create_centre():
    f = request.form
    image_file = request.files.get("image")

    # Normalize nullable / numeric fields
    def nn(v):  # None-or-number (float)
        return None if v == "" or v is None else float(v)
    def nni(v): # None-or-number (int)
        return None if v == "" or v is None else int(v)

    name = f.get("name","").strip()
    if not name:
        flash("Name is required.", "danger")
        return redirect(url_for("new_centre"))

    fields = {
        "city_id": int(f.get("city_id")),
        "classification_id": nni(f.get("classification_id")),
        "centre_type_id": nni(f.get("centre_type_id")),
        "name": name,
        "osm_name": f.get("osm_name","").strip() or None,
        "location": f.get("location","").strip() or None,
        "date_opened": f.get("date_opened") or None,
        "site_area_ha": nn(f.get("site_area_ha")),
        "covered_parking_num": nni(f.get("covered_parking_num")),
        "uncovered_parking_num": nni(f.get("uncovered_parking_num")),
        "redevelopments": f.get("redevelopments","").strip() or None,
        "levels": nni(f.get("levels")),
        "total_retail_space": nn(f.get("total_retail_space")),
    }

    # Insert basic row first to get id
    with db.get_cursor() as cur:
        cur.execute("""
            INSERT INTO shopping_centre
                (city_id, classification_id, centre_type_id, name, osm_name, location,
                 date_opened, site_area_ha, covered_parking_num, uncovered_parking_num,
                 redevelopments, levels, total_retail_space)
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            fields["city_id"], fields["classification_id"], fields["centre_type_id"],
            fields["name"], fields["osm_name"], fields["location"],
            fields["date_opened"], fields["site_area_ha"], fields["covered_parking_num"],
            fields["uncovered_parking_num"], fields["redevelopments"], fields["levels"],
            fields["total_retail_space"]
        ))
        centre_id = cur.lastrowid

        # Handle image upload (optional)
        if image_file and image_file.filename:
            os.makedirs(upload_dir(), exist_ok=True)
            new_filename = save_or_replace_image(centre_id, fields["name"], image_file)  # returns filename
            cur.execute("UPDATE shopping_centre SET image_filename=%s WHERE id=%s", (new_filename, centre_id))

    db.get_db().commit()
    flash("Centre created successfully.", "success")

    # If you search by osm_name on details page, use it; fall back to name
    search_key = fields["osm_name"] or fields["name"]
    return redirect(url_for("centredetails", name=search_key))
