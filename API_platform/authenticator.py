from functools import wraps
from flask import request, jsonify, Blueprint
import secrets
import qrcode

bp = Blueprint("authenticator", __name__, url_prefix="/auth")


@bp.route("register/webshop", methods=["GET"])
def register_webshop():
    return "register a webshop"


@bp.route("register/mobile_app", methods=["GET"])
def register_mobile_app_user():
    api_key = generate_key(16)
    generate_qr_code(api_key)
    return "html template pour afficher le qrcode"


def generate_key(length):
    return secrets.token_urlsafe(length)


def generate_qr_code(api_key):
    qr = qrcode.make(api_key)
    qr.save(f"API_platform/codes/{api_key}.png")


def has_too_many_requests(api_key):
    return False


def check_authentication(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("API_KEY") is None:
            return jsonify({"Error": "No validation key given. Access denied"}), 403
        api_key = request.headers.get("API_KEY")
        if api_key != "test":
            return jsonify({"Error": "Validation key not recognized. Access denied"}), 403
        if has_too_many_requests(api_key):
            return jsonify({"Error": "Too many requests. Try again later"}), 403
        return f(*args, **kwargs)

    return decorated_function
