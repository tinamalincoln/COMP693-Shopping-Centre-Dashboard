# app/src/route/auth.py
from flask import render_template, request, redirect, url_for, flash, g
from app import app, db
from app.src.model.auth import (
    get_user_by_username, verify_password, login_user, logout_user,
    is_admin, is_editor, set_password, create_user, delete_user, change_role
)


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")

        user = get_user_by_username(username)
        if not user or not verify_password(user["password_hash"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        login_user(user["id"])
        flash(f"Welcome, {user['first_name']}!", "success")
        # Redirect to where it makes sense (city summary)
        return redirect(url_for("city_summary"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    flash("You are now logged out.", "success")
    return redirect(url_for("city_summary"))



def _get_positions():
    """Return a simple list of distinct, non-empty positions for the datalist."""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT position
            FROM staff_user
            WHERE position IS NOT NULL AND TRIM(position) <> ''
            ORDER BY position ASC
        """)
        rows = cursor.fetchall()
    return [r["position"] for r in rows]

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not g.user:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))

    positions = _get_positions()

    if request.method == "POST":
        form_type = request.form.get("form", "").strip()

        # -------------------
        # Update details form
        # -------------------
        if form_type == "details":
            username    = (request.form.get("username") or "").strip()
            first_name  = (request.form.get("first_name") or "").strip()
            last_name   = (request.form.get("last_name") or "").strip()
            email       = (request.form.get("email") or "").strip()
            position    = (request.form.get("position") or "").strip() or None

            if not username or not first_name or not last_name or not email:
                flash("All required fields must be filled.", "danger")
            else:
                try:
                    with db.get_cursor() as cursor:
                        cursor.execute("""
                            UPDATE staff_user
                            SET username=%s, first_name=%s, last_name=%s,
                                email=%s, position=%s, updated_at=NOW()
                            WHERE id=%s
                        """, (username, first_name, last_name, email, position, g.user["id"]))
                    db.get_db().commit()
                    flash("Profile updated successfully.", "success")
                    return redirect(url_for("profile"))
                except Exception as e:
                    app.logger.exception("Failed to update profile")
                    flash("Could not update profile. Possibly duplicate username/email.", "danger")

        # --------------------
        # Update password form
        # --------------------
        elif form_type == "password":
            current_pw = (request.form.get("current_password") or "").strip()
            new_pw     = (request.form.get("new_password") or "").strip()
            confirm_pw = (request.form.get("confirm_password") or "").strip()

            if not current_pw or not new_pw or not confirm_pw:
                flash("Please fill in all password fields.", "danger")
            elif new_pw != confirm_pw:
                flash("New password and confirmation do not match.", "danger")
            elif len(new_pw) < 8:
                flash("New password must be at least 8 characters.", "danger")
            else:
                # Load current hash
                with db.get_cursor() as cursor:
                    cursor.execute("SELECT password_hash FROM staff_user WHERE id=%s", (g.user["id"],))
                    row = cursor.fetchone()

                if not row:
                    flash("Unable to verify current password.", "danger")
                elif not verify_password(row["password_hash"], current_pw):
                    flash("Current password is incorrect.", "danger")
                elif verify_password(row["password_hash"], new_pw):
                    flash("New password must be different from current password.", "danger")
                else:
                    # Update password via helper
                    set_password(g.user["id"], new_pw)
                    flash("Password updated successfully.", "success")
                    return redirect(url_for("profile"))

    return render_template("profile.html", user=g.user, positions=positions)

