import requests as r


def get_customers():
    try:
        result = r.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers')
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None


def get_customer_details(customer_id):
    try:
        result = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}")
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None


def get_customer_orders(customer_id):
    try:
        result = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}/orders")
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None


def get_customer_order_details(customer_id, order_id):
    try:
        result = r.get(
            f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}/orders/{order_id}/products")
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None
