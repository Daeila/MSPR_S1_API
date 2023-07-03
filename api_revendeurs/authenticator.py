from functools import wraps
from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for, session
from db.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from io import BytesIO
import jwt
import smtplib
import qrcode
import ssl

bp = Blueprint("authenticator", __name__, url_prefix="/auth")


def generate_token(payload):
    return jwt.encode(payload, "kawa_secret", algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, "kawa_secret", algorithms=["HS256"])
        return payload
    except(jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        return None


def send_token_via_email(token, to_email):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        msg = MIMEMultipart("related")
        msg["Subject"] = "Token d'identification à l'API revendeur"
        msg["From"] = "MSPR.API@gmail.com"
        msg["To"] = to_email
        msg.preamble = ""

        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)

        msg_text = MIMEText(f"<img src='cid:image1'></img> <div>{token}</div>", "html")
        msg_alternative.attach(msg_text)

        qc = qrcode.make(token)
        byte_buffer = BytesIO()
        qc.save(byte_buffer, "PNG")
        msg_image = MIMEImage(byte_buffer.getvalue(), "png")
        byte_buffer.close()

        msg_image.add_header("Content-ID", "<image1>")
        msg_alternative.attach(msg_image)

        msg_token = MIMEText(token, "plain")
        msg.attach(msg_token)

        msg.attach(msg_alternative)

        server.login("MSPR.API@gmail.com", "dhpluwgxenbfszjs")
        server.sendmail(msg["from"], msg["to"], msg.as_string())
        server.quit()


def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("TOKEN")
        if token is None:
            if session and "token" in session:
                token = session["token"]
            else:
                return jsonify({"Error": "No token given. Access denied"}), 403
        payload = decode_token(token)
        if payload is None:
            return jsonify({"Error": "Invalid token. Access denied"}), 403
        if "user_type" not in payload or "email" not in payload or "password" not in payload:
            return jsonify({"Error": "Token not recognized. Access denied"}), 403
        if payload["user_type"] != 1:
            return jsonify({"Error": "Invalid user type token. Access denied"}), 403
        db = get_db()
        user = db.execute(
            "SELECT email, password FROM Users WHERE email = ? AND user_type = 1",
            (payload["email"],)).fetchone()
        if user is None:
            return jsonify({"Error": "User not recognized. Access denied"}), 403
        if not check_password_hash(user["password"], payload["password"]):
            return jsonify({"Error": "Inorrect password. Access denied"}), 403
        return f(*args, **kwargs)

    return decorated_function


@bp.route("code", methods=["GET", "POST"])
def display_code():
    if request.method == "POST":
        logout_api_user()
    if session and "token" in session:
        return render_template("auth/qrcode.html", token=session["token"])
    else:
        return redirect(url_for("authenticator.login_api_user"))


@bp.route("login", methods=["GET", "POST"])
def login_api_user():
    if request.method == "POST":
        token = request.form["token"]

        error = None
        payload = decode_token(token)
        if not payload or "email" not in payload or "password" not in payload or "user_type" not in payload:
            error = "Token non valide"

        if error is None:
            db = get_db()
            user = None
            try:
                user = db.execute(
                    "SELECT email, password FROM Users WHERE email = ? AND user_type = 1",
                    (payload["email"],)).fetchone()
                if user is None:
                    error = "Email incorrect."
                elif not check_password_hash(user["password"], payload["password"]):
                    error = "Mot de passe incorrect."
                elif payload["user_type"] != 1:
                    error = "Type d'utilisateur incorrect."
            except db.IntegrityError:
                error = "Erreur db"

            if error is None:
                session.clear()
                session["email"] = user["email"]
                session["token"] = token

                return redirect(url_for("authenticator.display_code"))

        flash(error)

    return render_template("auth/login.html")


def logout_api_user():
    if session:
        session.clear()


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
                payload = {"email": email, "password": password, "user_type": 1}
                session["token"] = generate_token(payload)
                send_token_via_email(session["token"], session["email"])
                return redirect(url_for("authenticator.display_code"))

        flash(error)

    return render_template("auth/register.html")


def delete_user_from_db():
    pass
