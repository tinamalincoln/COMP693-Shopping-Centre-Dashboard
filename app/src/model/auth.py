# app/src/model/auth.py
from typing import Optional, Dict
from flask import session, g
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

def get_user_by_username(username: str) -> Optional[Dict]:
    with db.get_cursor() as cur:
        cur.execute("""
            SELECT id, username, password_hash, first_name, last_name, email, position, role, status
            FROM staff_user
            WHERE username=%s AND status='active'
        """, (username,))
        return cur.fetchone()

def verify_password(password_hash: str, password: str) -> bool:
    return check_password_hash(password_hash, password)

def set_password(user_id: int, new_password: str):
    with db.get_cursor() as cur:
        cur.execute("UPDATE staff_user SET password_hash=%s WHERE id=%s",
                    (generate_password_hash(new_password), user_id))
    db.get_db().commit()

def create_user(username, password, first_name, last_name, email, position, role):
    with db.get_cursor() as cur:
        cur.execute("""
            INSERT INTO staff_user (username, password_hash, first_name, last_name, email, position, role, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,'active')
        """, (username, generate_password_hash(password), first_name, last_name, email, position, role))
    db.get_db().commit()

def delete_user(user_id: int):
    with db.get_cursor() as cur:
        cur.execute("DELETE FROM staff_user WHERE id=%s", (user_id,))
    db.get_db().commit()

def change_role(user_id: int, role: str):
    with db.get_cursor() as cur:
        cur.execute("UPDATE staff_user SET role=%s WHERE id=%s", (role, user_id))
    db.get_db().commit()

def load_logged_in_user():
    """Call this in a before_request to populate g.user (or None)."""
    uid = session.get("user_id")
    if not uid:
        g.user = None
        return
    with db.get_cursor() as cur:
        cur.execute("""
            SELECT id, username, first_name, last_name, email, position, role, status
            FROM staff_user
            WHERE id=%s AND status='active'
        """, (uid,))
        g.user = cur.fetchone()

def login_user(user_id: int):
    session.clear()
    session["user_id"] = user_id

def logout_user():
    session.clear()

def is_editor() -> bool:
    return bool(getattr(g, "user", None) and g.user.get("role") in ("editor","admin"))

def is_admin() -> bool:
    return bool(getattr(g, "user", None) and g.user.get("role") == "admin")
