# app/src/route/centrecreate.py
from flask import render_template, request, redirect, url_for, flash
from app import app, db
from werkzeug.utils import secure_filename
from datetime import date
import os

# ---------- helpers ----------
def _coerce_none(v):
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
# ---------------------------------------------

@app.route("/centre/new", methods=["GET", "POST"])
def create_centre():
    if request.method == "POST":
        f = request.form
        image_file = request.files.get("image")

        # ----- City: accept city_id or free-text city_name -----
        city_id = _coerce_none(f.get("city_id"))
        city_name = _coerce_none(f.get("city_name"))  # from datalist text box

        with db.get_cursor() as cursor:
            if city_id:
                # optional: validate it exists
                cursor.execute("SELECT id, name FROM city WHERE id=%s", (city_id,))
                row = cursor.fetchone()
                if not row:
                    flash("Selected city not found.", "danger")
                    return redirect(url_for("create_centre"))
                resolved_city_name = row["name"]
            elif city_name:
                cursor.execute("SELECT id FROM city WHERE name=%s", (city_name,))
                row = cursor.fetchone()
                if row:
                    city_id = row["id"]
                else:
                    cursor.execute("INSERT INTO city (name) VALUES (%s)", (city_name,))
                    db.get_db().commit()
                    city_id = cursor.lastrowid
                resolved_city_name = city_name
            else:
                flash("Please select or type a city.", "danger")
                return redirect(url_for("create_centre"))

            # ----- Classification: text via datalist -----
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

            # ----- Centre type: text via datalist -----
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

            # ----- Other fields -----
            name        = _coerce_none(f.get("name"))
            if not name:
                flash("Centre name is required.", "danger")
                return redirect(url_for("create_centre"))

            osm_name    = _coerce_none(f.get("osm_name"))
            location    = _coerce_none(f.get("location"))
            date_opened = _coerce_none(f.get("date_opened"))
            if date_opened and date_opened > str(date.today()):
                flash("Date opened cannot be in the future.", "danger")
                return redirect(url_for("create_centre"))

            site_area_ha          = _coerce_decimal(f.get("site_area_ha"))
            covered               = _coerce_nonneg_int(f.get("covered_parking_num")) or 0
            uncovered             = _coerce_nonneg_int(f.get("uncovered_parking_num")) or 0
            redevelopments        = _coerce_none(f.get("redevelopments"))
            levels                = _coerce_nonneg_int(f.get("levels"))
            total_retail_space    = _coerce_decimal(f.get("total_retail_space"))

            # IMPORTANT: do NOT overwrite classification_id / centre_type_id from form here

            # ----- Insert the centre (image set after we know id) -----
            cursor.execute("""
                INSERT INTO shopping_centre
                (city_id, classification_id, centre_type_id, name, osm_name, location,
                 date_opened, site_area_ha, covered_parking_num, uncovered_parking_num,
                 redevelopments, levels, total_retail_space, image_filename)
                VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL)
            """, (
                city_id, classification_id, centre_type_id,
                name, osm_name, location,
                date_opened, site_area_ha, covered, uncovered,
                redevelopments, levels, total_retail_space
            ))
            db.get_db().commit()
            new_id = cursor.lastrowid

            # ----- Optional image upload -----
            if image_file and image_file.filename.strip():
                from app.src.model.image import upload_dir  # your helper
                upload_folder = upload_dir()  # resolves .../static/uploads/centre_photo
                os.makedirs(upload_folder, exist_ok=True)

                ext = secure_filename(image_file.filename).rsplit(".", 1)[-1].lower()
                filename = f"{name.replace(' ', '')}_{new_id}.{ext}"
                image_path = os.path.join(upload_folder, filename)
                image_file.save(image_path)

                cursor.execute(
                    "UPDATE shopping_centre SET image_filename=%s WHERE id=%s",
                    (filename, new_id)
                )
                db.get_db().commit()

        flash("New shopping centre created successfully.", "success")

        # Redirect to the city's centre list you just used/created
        return redirect(url_for("centrelist", city=resolved_city_name))

    # -------- GET: render form with datalists --------
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
        types=types,
        today_iso=date.today().isoformat(),
    )
