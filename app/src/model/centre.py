# app/src/model/centre.py

from app import app, db

def get_centre_by_osm(osm_name: str):
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT 
                sc.id, sc.name, sc.osm_name, sc.image_filename, sc.location,
                sc.total_retail_space, sc.date_opened, sc.site_area_ha,
                sc.covered_parking_num, sc.uncovered_parking_num, sc.redevelopments,
                sc.levels, sc.lat, sc.lon,
                c.name AS classification, t.name AS centre_type, ci.name AS city_name
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            LEFT JOIN city ci ON sc.city_id = ci.id
            WHERE sc.osm_name = %s
        """, (osm_name,))
        return cursor.fetchone()
