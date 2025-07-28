from flask import render_template, request
from app import app
from app.db import get_cursor
import requests
import urllib.parse

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search')
def search():
    q = request.args.get('q', '').strip()
    centre = None
    lat = lon = None
    searched = False

    if q:
        searched = True
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM shopping_centre WHERE name LIKE %s OR osm_name LIKE %s", (f"%{q}%", f"%{q}%"))
            centre = cursor.fetchone()

        if centre and centre.get('osm_name'):
            osm_query = urllib.parse.quote(centre['osm_name'])
            url = f"https://nominatim.openstreetmap.org/search?q={osm_query}+Christchurch&format=json&limit=1"
            headers = {'User-Agent': 'ShoppingCentreMapApp'}
            r = requests.get(url, headers=headers)
            if r.ok and r.json():
                lat = r.json()[0]['lat']
                lon = r.json()[0]['lon']
            else:
                centre = None  # Hide map if no coords found

    return render_template("search.html", centre=centre, lat=lat, lon=lon, searched=searched)
