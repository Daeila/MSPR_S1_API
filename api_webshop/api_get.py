from flask import Blueprint, g
from api_requests.crm import crm_requests as crm
from api_webshop.authenticator import check_authentication

bp = Blueprint("api_get", __name__, url_prefix="/")


@bp.route("customers", methods=["GET"])
@check_authentication
def get_customers():
    return crm.get_customers()


@bp.route("customers/<int:customer_id>", methods=["GET"])
@check_authentication
def get_customer_details(customer_id):
    return crm.get_customer_details(customer_id)


@bp.route("customers/<int:customer_id>/orders", methods=["GET"])
@check_authentication
def get_customer_orders(customer_id):
    return crm.get_customer_orders(customer_id)


@bp.route("customers/<int:customer_id>/orders/<int:order_id>/products", methods=["GET"])
@check_authentication
def get_customer_order_details(customer_id, order_id):
    return crm.get_customer_order_details(customer_id, order_id)
