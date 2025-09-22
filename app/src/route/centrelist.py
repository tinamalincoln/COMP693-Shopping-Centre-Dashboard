# app/src/route/centrelist.py
from flask import render_template, request, url_for
from app import app, db
import requests
from app.src.model.geo import geocode_centremap 

# Nominatim geocoding for city names
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
UA = {"User-Agent": "shopping-centre-dashboard/1.0 (educational use)"}

# Helper to geocode a city name via Nominatim
def geocode_city(city_name: str):
    """Return (lat, lon) for a NZ city via Nominatim, or None if not found."""
    if not city_name:
        return None
    params = {"q": f"{city_name}, New Zealand", "format": "json", "limit": 1}
    try:
        r = requests.get(NOMINATIM_URL, headers=UA, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None

# Centre list route
@app.route("/centres")
@app.route("/centres/<city>")
def centrelist(city=None):
    """
    List centres; if a city is provided, filter + center map on that city.
    Provides centres_for_map with sequential numbers for list + markers.
    """
    # Load centres (optionally filtered by city)
    with db.get_cursor() as cursor:
        if city:
            cursor.execute("""
                SELECT sc.id, sc.name, sc.osm_name, sc.location,
                       sc.lat, sc.lon,
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
                       sc.lat, sc.lon,
                       c.name AS classification, t.name AS centre_type, ci.name AS city_name
                FROM shopping_centre sc
                LEFT JOIN classification c ON sc.classification_id = c.id
                LEFT JOIN centre_type t   ON sc.centre_type_id = t.id
                LEFT JOIN city ci         ON sc.city_id = ci.id
                ORDER BY sc.name ASC
            """)
        centres = cursor.fetchall() or []

    # Choose current city label (for header + map centre)
    current_city = city
    if not current_city:
        current_city = centres[0]["city_name"] if centres and centres[0].get("city_name") else "Christchurch"

    # Geocode city for map centre (fallback: Christchurch)
    coords = geocode_city(current_city)
    if coords:
        default_lat, default_lon = coords
    else:
        default_lat, default_lon = (-43.5321, 172.6362)

    # Build centres_for_map with sequential numbers + geocoded coords
    centres_for_map = []
    for idx, row in enumerate(centres, start=1):
        # Ensure dict has the keys geocode_if_needed expects:
        # id, osm_name, city_name, lat, lon (optionally None)
        lat, lon = geocode_centremap(row)  # <- uses your dict-based function with DB caching

        # If not geocoded for some reason, skip marker (or keep None if you prefer)
        if lat is None or lon is None:
            continue
        
        # Append to list with sequential number
        centres_for_map.append({
            "id": row.get("id"),
            "number": idx,
            "name": row.get("name") or "",
            "osm_name": row.get("osm_name") or "",
            "location": row.get("location") or "",
            "lat": float(lat),
            "lon": float(lon),
            # Link to detail page: keep 'search' unless you've renamed the endpoint
            "details_url": url_for("centredetails", name=row.get("osm_name") or "")
        })

    # Render
    return render_template(
        "centrelist.html",
        centres=centres,
        centres_for_map=centres_for_map,
        lat=default_lat,
        lon=default_lon,
        current_city=current_city
    )
