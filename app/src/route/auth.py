# app/src/route/auth.py
from flask import render_template, request, redirect, url_for, flash, g
from app import app
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

@app.route("/profile", methods=["GET","POST"])
def profile():
    if not g.user:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        new_pw = request.form.get("new_password","").strip()
        if not new_pw:
            flash("Password cannot be empty.", "danger")
        else:
            set_password(g.user["id"], new_pw)
            flash("Password updated.", "success")
            return redirect(url_for("profile"))

    return render_template("profile.html")

# Admin-only staff management
@app.route("/staff", methods=["GET","POST"])
def staff_admin():
    if not is_admin():
        flash("Admins only.", "danger")
        return redirect(url_for("city_summary"))

    from app import db
    if request.method == "POST":
        action = request.form.get("action")
        if action == "create":
            create_user(
                request.form["username"].strip(),
                request.form["password"],
                request.form["first_name"].strip(),
                request.form["last_name"].strip(),
                request.form["email"].strip(),
                request.form.get("position"),
                request.form.get("role")
            )
            flash("User created.", "success")
        elif action == "delete":
            delete_user(int(request.form["user_id"]))
            flash("User deleted.", "success")
        elif action == "changerole":
            change_role(int(request.form["user_id"]), request.form["role"])
            flash("Role updated.", "success")
        return redirect(url_for("staff_admin"))

    with db.get_cursor() as cur:
        cur.execute("""
            SELECT id, username, first_name, last_name, email, position, role, status, created_at
            FROM staff_user ORDER BY created_at DESC
        """)
        users = cur.fetchall()
    return render_template("staff_admin.html", users=users)
