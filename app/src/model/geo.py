# app/src/model/geo.py

from app import app, db
import requests


def geocode_if_needed(centre: dict):
    """
    Prefer cached lat/lon from DB. If missing, geocode once and save lat/lon.
    """
    if centre.get('lat') is not None and centre.get('lon') is not None:
        return float(centre['lat']), float(centre['lon'])

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

    resp = requests.get(url, headers={"User-Agent": "shopping-centre-dashboard"}, params=params, timeout=15)

    if resp.status_code == 200 and resp.json():
        lat = float(resp.json()[0]["lat"])
        lon = float(resp.json()[0]["lon"])
        # cache into DB so we don't geocode again next time
        with db.get_cursor() as cursor:
            cursor.execute("UPDATE shopping_centre SET lat=%s, lon=%s WHERE id=%s", (lat, lon, centre['id']))
        db.get_db().commit()
        return lat, lon

    # fallback to Christchurch CBD
    return -43.5321, 172.6362

def build_ors_reach_url(lat: float, lon: float, zoom: int = 15) -> str:
    return (
        f"https://classic-maps.openrouteservice.org/reach"
        f"?n1={lat}&n2={lon}&n3={zoom}&a={lat},{lon}&b=0&i=0&j1=10&j2=2&k1=en-US&k2=km"
    )

