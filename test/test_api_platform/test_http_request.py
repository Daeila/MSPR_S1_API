import unittest
import requests


class TestsHttpRequests(unittest.TestCase):
    URLs = {
        "root": "http://localhost:5000/",
        "products": "http://localhost:5000/products",
        "product_details": "http://localhost:5000/products/{}",
        "customers": "http://localhost:5000/customers",
        "customer_orders": "http://localhost:5000/customers/{}/orders",
        "customer_order_details": "http://localhost:5000/customers/{}/orders/{}/products"
    }

    def test_get_products(self):
        response = requests.get(self.URLs["products"]).text
        self.assertEqual(response, "list of all products")

    def test_get_product_details(self):
        product_id = 1
        response = requests.get(self.URLs["product_details"].format(product_id)).text
        self.assertEqual(response, f"product id no {product_id}")

    def test_get_customers(self):
        response = requests.get(self.URLs["customers"]).text
        self.assertEqual(response, "list of all customers")

    def test_get_customer_orders(self):
        customer_id = 1
        response = requests.get(self.URLs["customer_orders"].format(customer_id)).text
        self.assertEqual(response, f"orders from customer no {customer_id}")

    def test_get_customer_order_details(self):
        order_id = 1
        customer_id = 2
        response = requests.get(self.URLs["customer_order_details"].format(customer_id, order_id)).text
        self.assertEqual(response, f"order no {order_id} from customer no {customer_id}")


if __name__ == "__main__":
    TestsHttpRequests()
