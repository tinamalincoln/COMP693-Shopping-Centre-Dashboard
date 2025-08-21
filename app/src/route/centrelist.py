# app/src/route/centrelist.py
from flask import render_template, request
from app import app, db
import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
UA = {"User-Agent": "shopping-centre-dashboard/1.0 (educational use)"}

def geocode_city(city_name: str):
    """Return (lat, lon) for a NZ city via Nominatim, or None if not found."""
    if not city_name:
        return None
    params = {
        "q": f"{city_name}, New Zealand",
        "format": "json",
        "limit": 1,
    }
    try:
        r = requests.get(NOMINATIM_URL, headers=UA, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

@app.route("/centres")
@app.route("/centres/<city>")
def centrelist(city=None):
    """List centres; if a city is provided, filter + center map on that city."""
    # 1) Load list of centres (optionally filtered by city)
    with db.get_cursor() as cursor:
        if city:
            cursor.execute("""
                SELECT sc.id, sc.name, sc.osm_name, sc.location,
                       c.name AS classification, t.name AS centre_type, ci.name AS city_name
                FROM shopping_centre sc
                LEFT JOIN classification c ON sc.classification_id = c.id
                LEFT JOIN centre_type t   ON sc.centre_type_id = t.id
                LEFT JOIN city ci         ON sc.city_id = ci.id
                WHERE ci.name = %s
                ORDER BY sc.name ASC
            """, (city,))
        else:
            cursor.execute("""
                SELECT sc.id, sc.name, sc.osm_name, sc.location,
                       c.name AS classification, t.name AS centre_type, ci.name AS city_name
                FROM shopping_centre sc
                LEFT JOIN classification c ON sc.classification_id = c.id
                LEFT JOIN centre_type t   ON sc.centre_type_id = t.id
                LEFT JOIN city ci         ON sc.city_id = ci.id
                ORDER BY sc.name ASC
            """)
        centres = cursor.fetchall()

    # 2) Figure out which city label to show in header
    current_city = city
    if not current_city:
        # If city not explicitly given, infer from first centre (if any)
        if centres and centres[0].get("city_name"):
            current_city = centres[0]["city_name"]
        else:
            current_city = "Christchurch"

    # 3) Geocode the current city for the map center
    coords = geocode_city(current_city)
    if coords:
        default_lat, default_lon = coords
    else:
        # Safe fallback
        default_lat, default_lon = (-43.5321, 172.6362)  # Christchurch

    return render_template(
        "centrelist.html",
        centres=centres,
        lat=default_lat,
        lon=default_lon,
        current_city=current_city
    )
