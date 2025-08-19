# app/src/route/centrecreate.py
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from werkzeug.utils import secure_filename
import os
from datetime import date

def _coerce_none(v):
    # Turn empty strings into None
    return v if (v is not None and str(v).strip() != "") else None

def _coerce_nonneg_int(v):
    v = _coerce_none(v)
    if v is None:
        return None
    try:
        iv = int(v)
        return iv if iv >= 0 else 0
    except:
        return None

def _coerce_decimal(v):
    v = _coerce_none(v)
    if v is None:
        return None
    try:
        return float(v)
    except:
        return None

@app.route("/centre/new", methods=["GET", "POST"])
def create_centre():
    if request.method == "POST":
        f = request.form
        image_file = request.files.get("image")

        # 1) City resolution: support either city_id OR free-text city_name
        city_id = _coerce_none(f.get("city_id"))
        city_name = _coerce_none(f.get("city_name"))  # from a <input list="...">

        with db.get_cursor() as cursor:
            if city_id:
                # trust the selected id (but you can validate it exists)
                pass
            elif city_name:
                # look up by name; insert if missing
                cursor.execute("SELECT id FROM city WHERE name=%s", (city_name,))
                row = cursor.fetchone()
                if row:
                    city_id = row["id"]
                else:
                    cursor.execute("INSERT INTO city (name) VALUES (%s)", (city_name,))
                    db.get_db().commit()
                    city_id = cursor.lastrowid
            else:
                flash("Please select or type a city.", "danger")
                return redirect(url_for("create_centre"))

                        # --- Classification resolution (new or existing) ---
            classification_name = _coerce_none(f.get("classification_name"))
            if not classification_name:
                flash("Please enter or select a classification.", "danger")
                return redirect(url_for("create_centre"))

            cursor.execute("SELECT id FROM classification WHERE name=%s", (classification_name,))
            row = cursor.fetchone()
            if row:
                classification_id = row["id"]
            else:
                cursor.execute("INSERT INTO classification (name) VALUES (%s)", (classification_name,))
                db.get_db().commit()
                classification_id = cursor.lastrowid

            # --- Centre Type resolution (new or existing) ---
            centre_type_name = _coerce_none(f.get("centre_type_name"))
            if not centre_type_name:
                flash("Please enter or select a centre type.", "danger")
                return redirect(url_for("create_centre"))

            cursor.execute("SELECT id FROM centre_type WHERE name=%s", (centre_type_name,))
            row = cursor.fetchone()
            if row:
                centre_type_id = row["id"]
            else:
                cursor.execute("INSERT INTO centre_type (name) VALUES (%s)", (centre_type_name,))
                db.get_db().commit()
                centre_type_id = cursor.lastrowid

            
            
            
            # 2) Other fields (coerce empties safely)
            name = _coerce_none(f.get("name"))
            osm_name = _coerce_none(f.get("osm_name"))
            location = _coerce_none(f.get("location"))
            date_opened = _coerce_none(f.get("date_opened"))
            # Optional: block future dates server-side
            if date_opened and date_opened > str(date.today()):
                flash("Date opened cannot be in the future.", "danger")
                return redirect(url_for("create_centre"))

            site_area_ha = _coerce_decimal(f.get("site_area_ha"))
            covered = _coerce_nonneg_int(f.get("covered_parking_num"))
            uncovered = _coerce_nonneg_int(f.get("uncovered_parking_num"))
            redevelopments = _coerce_none(f.get("redevelopments"))
            levels = _coerce_nonneg_int(f.get("levels"))
            total_retail_space = _coerce_decimal(f.get("total_retail_space"))
            classification_id = _coerce_none(f.get("classification_id"))
            centre_type_id = _coerce_none(f.get("centre_type_id"))

            if not name:
                flash("Centre name is required.", "danger")
                return redirect(url_for("create_centre"))

            # 3) Insert centre row (image to be added after we get id)
            cursor.execute("""
                INSERT INTO shopping_centre
                (city_id, classification_id, centre_type_id, name, osm_name, location,
                 date_opened, site_area_ha, covered_parking_num, uncovered_parking_num,
                 redevelopments, levels, total_retail_space)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                city_id, classification_id, centre_type_id, name, osm_name, location,
                date_opened, site_area_ha, covered, uncovered, redevelopments, levels, total_retail_space
            ))
            db.get_db().commit()
            new_id = cursor.lastrowid

            # 4) Optional image upload
            if image_file and image_file.filename.strip():
                from app.src.model.image import upload_dir  # your helper
                upload_folder = upload_dir()
                os.makedirs(upload_folder, exist_ok=True)

                # Save as NameWithoutSpaces_ID.ext
                ext = image_file.filename.rsplit(".", 1)[-1].lower()
                new_filename = f"{name.replace(' ', '')}_{new_id}.{ext}"
                path = os.path.join(upload_folder, new_filename)
                image_file.save(path)

                cursor.execute(
                    "UPDATE shopping_centre SET image_filename=%s WHERE id=%s",
                    (new_filename, new_id)
                )
                db.get_db().commit()

        flash("New shopping centre created successfully.", "success")
        # Redirect to details using osm_name (like your existing flow)
        return redirect(url_for("city_summary", name=osm_name or name))

    # GET: load dropdown lists
    with db.get_cursor() as cursor:
        cursor.execute("SELECT id, name FROM city ORDER BY name;")
        cities = cursor.fetchall()
        cursor.execute("SELECT id, name FROM classification ORDER BY name;")
        classifications = cursor.fetchall()
        cursor.execute("SELECT id, name FROM centre_type ORDER BY name;")
        types = cursor.fetchall()

    return render_template(
        "centrenew.html",
        cities=cities,
        classifications=classifications,
        types=types
    )
