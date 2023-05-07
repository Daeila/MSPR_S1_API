from flask import Blueprint, g
from api_requests.crm import crm_requests as crm
from api_webshop.authenticator import check_authentication

bp = Blueprint("api_get", __name__, url_prefix="/")


@bp.route("customers", methods=["GET"])
def get_customers():
    result = crm.get_customers()
    if result:
        return result
    else:
        return "Invalid request"


@bp.route("customers/<int:customer_id>", methods=["GET"])
def get_customer_details(customer_id):
    result = crm.get_customer_details(customer_id)
    if result:
        return result
    else:
        return "Invalid request"


@bp.route("customers/<int:customer_id>/orders", methods=["GET"])
def get_customer_orders(customer_id):
    result = crm.get_customer_orders(customer_id)
    if result:
        return result
    else:
        return "Invalid request"


@bp.route("customers/<int:customer_id>/orders/<int:order_id>/products", methods=["GET"])
def get_customer_order_details(customer_id, order_id):
    result = crm.get_customer_order_details(customer_id, order_id)
    if result:
        return result
    else:
        return "Invalid request"
