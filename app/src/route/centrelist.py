# app/src/route/centrelist.py
from flask import render_template, request
from app import app, db

@app.route("/centrelist")
def centrelist():
    city = request.args.get("city")

    with db.get_cursor() as cursor:
        if city:
            cursor.execute("""
                SELECT 
                    sc.id, sc.name, sc.osm_name, sc.location,
                    c.name AS classification, t.name AS centre_type, ci.name AS city
                FROM shopping_centre sc
                LEFT JOIN classification c ON sc.classification_id = c.id
                LEFT JOIN centre_type t ON sc.centre_type_id = t.id
                JOIN city ci ON sc.city_id = ci.id
                WHERE ci.name = %s
                ORDER BY sc.name ASC
            """, (city,))
        else:
            cursor.execute("""
                SELECT 
                    sc.id, sc.name, sc.osm_name, sc.location,
                    c.name AS classification, t.name AS centre_type, ci.name AS city
                FROM shopping_centre sc
                LEFT JOIN classification c ON sc.classification_id = c.id
                LEFT JOIN centre_type t ON sc.centre_type_id = t.id
                JOIN city ci ON sc.city_id = ci.id
                ORDER BY sc.name ASC
            """)
        centres = cursor.fetchall()

    default_lat, default_lon = -43.5321, 172.6362
    return render_template("centrelist.html", centres=centres, lat=default_lat, lon=default_lon, city=city)
