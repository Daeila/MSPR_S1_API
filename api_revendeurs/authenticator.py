from functools import wraps
from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for, session
from db.db import get_db
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

bp = Blueprint("authenticator", __name__, url_prefix="/auth")


def generate_key(length):
    return secrets.token_urlsafe(length)


def has_too_many_requests(api_key):
    return False


def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("API_KEY")
        if api_key is None:
            if session and "api_key" in session:
                api_key = session["api_key"]
            else:
                return jsonify({"Error": "No validation key given. Access denied"}), 403
        db = get_db()
        user = db.execute(
            "SELECT k.api_key FROM Keys k WHERE api_key = ?",
            (api_key,)).fetchone()
        if user is None:
            return jsonify({"Error": "Validation key not recognized. Access denied"}), 403
        if has_too_many_requests(api_key):
            return jsonify({"Error": "Too many requests. Try again later"}), 403
        return f(*args, **kwargs)

    return decorated_function


@bp.route("key", methods=["GET"])
def display_key():
    if session and "api_key" in session:
        return render_template("auth/qrcode.html", api_key=session["api_key"])
    else:
        return url_for("authenticator.login_api_user")


@bp.route("login", methods=["GET", "POST"])
def login_api_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None

        user = db.execute(
            "SELECT u.email, u.password, k.api_key FROM Users u LEFT JOIN Keys k ON (u.id = k.user_id) WHERE email = ?",
            (email,)).fetchone()
        if user is None:
            error = "Email incorrect."
        elif not check_password_hash(user["password"], password):
            error = "Mot de passe incorrect."

        if error is None:
            session.clear()
            session["email"] = user["email"]
            session["api_key"] = user["api_key"]

            return redirect(url_for("authenticator.display_key"))

        flash(error)

    return render_template("auth/login.html")


def logout_api_user():
    pass


@bp.route("register", methods=["GET", "POST"])
def register_api_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not email:
            error = "Veuillez fournir un email."
        elif not password:
            error = "Veuillez fournir un mot de passe."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO Users (email, password, user_type) VALUES(?, ?, 1)",
                    (email, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f"L'email {email} existe déjà."
            else:
                session.clear()
                session["email"] = email
                session["api_key"] = generate_key(16)
                try:
                    user = db.execute(
                        "SELECT id FROM Users WHERE email = ?", (email,)).fetchone()
                    db.execute(
                        "INSERT INTO Keys (user_id, api_key, key_creation_date) VALUES(?, ?, ?)",
                        (user["id"], session["api_key"], str(datetime.now().time())))
                    db.commit()
                except db.IntegrityError:
                    error = "Erreur lors de l'enregistrement des données."
                else:
                    return redirect(url_for("authenticator.display_key"))

        flash(error)

    return render_template("auth/register.html")


def delete_user_from_db():
    pass
