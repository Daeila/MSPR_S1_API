from flask import Blueprint, g
from api_requests.erp import erp_requests as erp
from api_revendeurs.authenticator import check_authentication

bp = Blueprint("api_get", __name__, url_prefix="/")


@bp.route("products", methods=["GET"])
@check_authentication
def get_products():
    return erp.get_products()


@check_authentication
@bp.route("products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    return erp.get_product_details(product_id)
