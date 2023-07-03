import requests as r


def get_products():
    try:
        result = r.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products')
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None


def get_product_details(product_id):
    try:
        result = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}")
        if result:
            return result.json()
        else:
            return {}
    except r.exceptions.JSONDecodeError:
        return None
