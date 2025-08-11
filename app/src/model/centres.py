# app/src/model/centres.py

from app import app, db

def list_centres():
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT sc.id, sc.name, sc.osm_name, sc.location,
                   c.name AS classification, t.name AS centre_type
            FROM shopping_centre sc
            LEFT JOIN classification c ON sc.classification_id = c.id
            LEFT JOIN centre_type t ON sc.centre_type_id = t.id
            ORDER BY sc.name ASC
        """)
        return cursor.fetchall()

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


def update_centre(centre_id: int, fields: dict):
    with db.get_cursor() as cursor:
        cursor.execute("""
            UPDATE shopping_centre
            SET name=%s, osm_name=%s, location=%s, date_opened=%s, site_area_ha=%s,
                covered_parking_num=%s, uncovered_parking_num=%s, redevelopments=%s,
                levels=%s, total_retail_space=%s
            WHERE id=%s
        """, (
            fields["name"], fields["osm_name"], fields["location"], fields["date_opened"],
            fields["site_area_ha"], fields["covered_parking_num"], fields["uncovered_parking_num"],
            fields["redevelopments"], fields["levels"], fields["total_retail_space"], centre_id
        ))
    db.get_db().commit()


def set_image_filename(centre_id: int, filename: str):
    with db.get_cursor() as cursor:
        cursor.execute("UPDATE shopping_centre SET image_filename=%s WHERE id=%s", (filename, centre_id))
    db.get_db().commit()

def get_image_filename(centre_id: int):
    with db.get_cursor() as cursor:
        cursor.execute("SELECT image_filename FROM shopping_centre WHERE id=%s", (centre_id,))
        row = cursor.fetchone()
        return row.get("image_filename") if row else None

def delete_centre(centre_id: int):
    with db.get_cursor() as cursor:
        cursor.execute("DELETE FROM shopping_centre WHERE id=%s", (centre_id,))
    db.get_db().commit()
