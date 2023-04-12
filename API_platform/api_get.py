from flask import jsonify, Blueprint

bp = Blueprint("api_get", __name__, url_prefix="/")


@bp.route("products", methods=["GET"])
def get_products():
    return "list of all products"


@bp.route("products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    return f"product id no {product_id}"


@bp.route("customers", methods=["GET"])
def get_customers():
    return "list of all customers"


@bp.route("customers/<int:customer_id>/orders", methods=["GET"])
def get_customer_orders(customer_id):
    return f"orders from customer no {customer_id}"


@bp.route("customers/<int:customer_id>/orders/<int:order_id>/products", methods=["GET"])
def get_customer_order_details(customer_id, order_id):
    return f"order no {order_id} from customer no {customer_id}"
