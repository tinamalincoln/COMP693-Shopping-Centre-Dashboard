from flask import render_template
from app import app, db
import os
from dotenv import load_dotenv

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

@app.route("/")
def home():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                sc.id, sc.name, sc.osm_name, sc.location,
                c.name AS classification, t.name AS centre_type
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            ORDER BY sc.name ASC
        """)
        centres = cursor.fetchall()

    default_lat, default_lon = -43.5321, 172.6362
    return render_template("home.html", centres=centres, lat=default_lat, lon=default_lon)

