import requests as r


def get_customers():
    return r.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers').json()


def get_customer_details(customer_id):
    return r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}").json()


def get_customer_orders(customer_id):
    return r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}/orders").json()


def get_customer_order_details(customer_id, order_id):
    return r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers/{customer_id}/orders/{order_id}").json()
