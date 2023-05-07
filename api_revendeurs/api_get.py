from flask import Blueprint, g
from api_revendeurs.authenticator import check_authentication

bp = Blueprint("api_get", __name__, url_prefix="/")


@bp.route("products", methods=["GET"])
def get_products():
    return "list of all products"


@bp.route("products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    return f"product id no {product_id}"
