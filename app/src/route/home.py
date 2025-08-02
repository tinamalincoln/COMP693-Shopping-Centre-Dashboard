from flask import render_template, request
from app import app, db
import requests

@app.route("/")
def home():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                sc.name, sc.osm_name, sc.location,
                c.name AS classification, t.name AS centre_type
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            ORDER BY sc.name ASC
        """)
        centres = cursor.fetchall()

    # Default location to center map on Christchurch
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
                sc.name, sc.osm_name, sc.location, sc.total_retail_space, sc.date_opened, sc.site_area_ha, 
                sc.covered_parking_num, sc.uncovered_parking_num, sc.redevelopments, sc.levels,
                c.name AS classification, t.name AS centre_type
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            WHERE sc.osm_name = %s
        """, (centre_name,))
        centre = cursor.fetchone()

    if not centre:
        return render_template("search.html", error="Shopping centre not found.")

    query = centre['osm_name']
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query + ", Christchurch, New Zealand",
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, headers={"User-Agent": "shopping-centre-dashboard"}, params=params)

    if response.status_code == 200 and response.json():
        location = response.json()[0]
        lat, lon = float(location["lat"]), float(location["lon"])
    else:
        lat, lon = -43.5321, 172.6362

    return render_template("search.html", centre=centre, lat=lat, lon=lon)
