import requests as r


def get_products():
    return r.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products').json()


def get_product_details(product_id):
    return r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}").json()
