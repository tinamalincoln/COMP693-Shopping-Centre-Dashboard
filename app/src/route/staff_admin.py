from flask import render_template, request, redirect, url_for, flash, g
from app import app, db
from werkzeug.security import generate_password_hash
from datetime import datetime

# ---------- helpers ----------
def _require_admin():
    if not getattr(g, "user", None) or g.user.get("role") != "admin":
        flash("Admin access required.", "danger")
        return False
    return True

def _get_positions():
    with db.get_cursor() as cur:
        cur.execute("""
            SELECT DISTINCT position
            FROM staff_user
            WHERE position IS NOT NULL AND TRIM(position) <> ''
            ORDER BY position ASC
        """)
        rows = cur.fetchall()
    return [r["position"] for r in rows]

# ---------- pages ----------
@app.route("/staff-admin")
def staff_admin():
    if not _require_admin(): 
        return redirect(url_for("login"))

    q = (request.args.get("q") or "").strip()
    with db.get_cursor() as cur:
        if q:
            cur.execute("""
                SELECT id, username, first_name, last_name, email, position, role, status, created_at, updated_at
                FROM staff_user
                WHERE username LIKE %s OR first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
                ORDER BY created_at DESC
            """, (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%"))
        else:
            cur.execute("""
                SELECT id, username, first_name, last_name, email, position, role, status, created_at, updated_at
                FROM staff_user
                ORDER BY created_at DESC
            """)
        staff = cur.fetchall()

    return render_template(
        "manage_staff.html",
        staff=staff,
        positions=_get_positions(),
    )

# Create staff (admin or editor)
@app.route("/staff-admin/create", methods=["POST"])
def create_staff():
    if not _require_admin(): 
        return redirect(url_for("login"))

    f = request.form
    username   = (f.get("username") or "").strip()
    first_name = (f.get("first_name") or "").strip()
    last_name  = (f.get("last_name") or "").strip()
    email      = (f.get("email") or "").strip()
    position   = (f.get("position") or "").strip() or None
    role       = (f.get("role") or "editor").strip().lower()
    status     = (f.get("status") or "active").strip().lower()
    password   = (f.get("password") or "").strip()

    if not username or not email or not password or role not in ("admin","editor") or status not in ("active","inactive"):
        flash("Please complete all required fields (username, email, password) and valid role/status.", "danger")
        return redirect(url_for("staff_admin"))

    try:
        pw_hash = generate_password_hash(password)
        with db.get_cursor() as cur:
            cur.execute("""
                INSERT INTO staff_user
                    (username, password_hash, first_name, last_name, email, position, role, status, created_at, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
            """, (username, pw_hash, first_name, last_name, email, position, role, status))
        db.get_db().commit()
        flash(f"User “{username}” created.", "success")
    except Exception as e:
        app.logger.exception("Create staff failed")
        flash("Could not create user (possibly duplicate username or email).", "danger")

    return redirect(url_for("staff_admin"))

# Update role/status/position/name/email/username (and optional password reset)
@app.route("/staff-admin/<int:user_id>/update", methods=["POST"])
def update_staff(user_id):
    if not _require_admin(): 
        return redirect(url_for("login"))

    if g.user["id"] == user_id and request.form.get("role","editor") != "admin":
        flash("You cannot demote yourself from admin.", "warning")
        return redirect(url_for("staff_admin"))

    f = request.form
    username   = (f.get("username") or "").strip()
    first_name = (f.get("first_name") or "").strip()
    last_name  = (f.get("last_name") or "").strip()
    email      = (f.get("email") or "").strip()
    position   = (f.get("position") or "").strip() or None
    role       = (f.get("role") or "").strip().lower()
    status     = (f.get("status") or "").strip().lower()
    new_pw     = (f.get("new_password") or "").strip()

    if role not in ("admin","editor") or status not in ("active","inactive"):
        flash("Invalid role/status.", "danger")
        return redirect(url_for("staff_admin"))

    try:
        with db.get_cursor() as cur:
            if new_pw:
                cur.execute("""
                    UPDATE staff_user
                    SET username=%s, first_name=%s, last_name=%s, email=%s,
                        position=%s, role=%s, status=%s, password_hash=%s, updated_at=NOW()
                    WHERE id=%s
                """, (username, first_name, last_name, email, position, role, status,
                      generate_password_hash(new_pw), user_id))
            else:
                cur.execute("""
                    UPDATE staff_user
                    SET username=%s, first_name=%s, last_name=%s, email=%s,
                        position=%s, role=%s, status=%s, updated_at=NOW()
                    WHERE id=%s
                """, (username, first_name, last_name, email, position, role, status, user_id))
        db.get_db().commit()
        flash("User updated.", "success")
    except Exception:
        app.logger.exception("Update staff failed")
        flash("Could not update user (possibly duplicate username or email).", "danger")

    return redirect(url_for("staff_admin"))

# Delete user
@app.route("/staff-admin/<int:user_id>/delete", methods=["POST"])
def delete_staff(user_id):
    if not _require_admin(): 
        return redirect(url_for("login"))

    if g.user["id"] == user_id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("staff_admin"))

    try:
        with db.get_cursor() as cur:
            cur.execute("SELECT username, role FROM staff_user WHERE id=%s", (user_id,))
            row = cur.fetchone()
            if not row:
                flash("User not found.", "warning")
                return redirect(url_for("staff_admin"))

            # Optional safety: prevent deleting last remaining admin
            if row["role"] == "admin":
                cur.execute("SELECT COUNT(*) AS c FROM staff_user WHERE role='admin' AND status='active'")
                c = cur.fetchone()["c"]
                if c <= 1:
                    flash("Cannot delete the last active admin.", "warning")
                    return redirect(url_for("staff_admin"))

            cur.execute("DELETE FROM staff_user WHERE id=%s", (user_id,))
        db.get_db().commit()
        flash(f"User “{row['username']}” deleted.", "success")
    except Exception:
        app.logger.exception("Delete staff failed")
        flash("Could not delete user.", "danger")

    return redirect(url_for("staff_admin"))
