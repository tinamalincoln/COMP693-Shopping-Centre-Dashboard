# app/src/route/centrelist.py

from flask import render_template
from app import app, db
import os
from dotenv import load_dotenv
from app.src.model.centres import list_centres

load_dotenv()
ORS_API_KEY = os.getenv("ORS_API_KEY")

@app.route("/")
def centrelist():
    centres = list_centres()
    default_lat, default_lon = -43.5321, 172.6362
    return render_template("home.html", centres=centres, lat=default_lat, lon=default_lon)

