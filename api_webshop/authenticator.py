from functools import wraps
from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for, session
from db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
import jwt

bp = Blueprint("authenticator", __name__, url_prefix="/auth")


def generate_token(payload):
    return jwt.encode(payload, "kawa_secret", algorithm="HS256")


def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("TOKEN")
        if token is None:
            if session and "token" in session:
                token = session["token"]
            else:
                return jsonify({"Error": "No token given. Access denied"}), 403
        try:
            payload = jwt.decode(token, "kawa_secret", algorithms=["HS256"])
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
            return jsonify({"Error": "Invalid token. Access denied"}), 403
        if "user_type" not in payload or "email" not in payload:
            return jsonify({"Error": "Token not recognized. Access denied"}), 403
        if payload["user_type"] != 1:
            return jsonify({"Error": "Invalid user type token. Access denied"}), 403
        db = get_db()
        user = db.execute(
            "SELECT email FROM Users WHERE email = ?",
            (payload["email"],)).fetchone()
        if user is None:
            return jsonify({"Error": "User not recognized. Access denied"}), 403
        return f(*args, **kwargs)

    return decorated_function


@bp.route("code", methods=["GET"])
def display_code():
    if session and "token" in session:
        return render_template("auth/qrcode.html", token=session["token"])
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
            "SELECT email, password FROM Users WHERE email = ?",
            (email,)).fetchone()
        if user is None:
            error = "Email incorrect."
        elif not check_password_hash(user["password"], password):
            error = "Mot de passe incorrect."

        if error is None:
            session.clear()
            session["email"] = user["email"]

            return redirect(url_for("authenticator.display_code"))

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
                    "INSERT INTO Users (email, password, user_type) VALUES(?, ?, 2)",
                    (email, generate_password_hash(password)))
                db.commit()
            except db.IntegrityError:
                error = f"L'email {email} existe déjà."
            else:
                session.clear()
                session["email"] = email
                payload = {"email": session["email"], "user_type": 1}
                session["token"] = generate_token(payload)
                return redirect(url_for("authenticator.display_code"))

        flash(error)

    return render_template("auth/register.html")


def delete_user_from_db():
    pass
