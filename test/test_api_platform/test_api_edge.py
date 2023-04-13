import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class PageObject:
    URLs = {
        "root": "http://localhost:5000/",
        "products": "http://localhost:5000/products",
        "product_details": "http://localhost:5000/products/{}",
        "customers": "http://localhost:5000/customers",
        "customer_orders": "http://localhost:5000/customers/{}/orders",
        "customer_order_details": "http://localhost:5000/customers/{}/orders/{}/products"
    }

    def __init__(self, driver_):
        self.driver = driver_

    def go_to_root(self):
        url = self.URLs["root"]
        self.driver.get(url)

    def go_to_products(self):
        url = self.URLs["products"]
        self.driver.get(url)

    def go_to_product_details(self, product_id):
        url = self.URLs["product_details"].format(product_id)
        self.driver.get(url)

    def go_to_customers(self):
        url = self.URLs["customers"]
        self.driver.get(url)

    def go_to_customer_orders(self, customer_id):
        url = self.URLs["customer_orders"].format(customer_id)
        self.driver.get(url)

    def go_to_customer_order_details(self, customer_id, order_id):
        url = self.URLs["customer_order_details"].format(customer_id, order_id)
        self.driver.get(url)


class TestsEdge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            options=webdriver.EdgeOptions(),
        )
        cls.driver.maximize_window()
        cls.app = PageObject(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_go_to_products(self):
        self.app.go_to_products()
        text_on_page = self.driver.find_element(by=By.TAG_NAME, value="body").get_attribute("innerHTML")
        self.assertEqual(text_on_page, "list of all products")

    def test_go_to_product_details(self):
        product_id = 1
        self.app.go_to_product_details(product_id)
        text_on_page = self.driver.find_element(by=By.TAG_NAME, value="body").get_attribute("innerHTML")
        self.assertEqual(text_on_page, f"product id no {product_id}")

    def test_go_to_customers(self):
        self.app.go_to_customers()
        text_on_page = self.driver.find_element(by=By.TAG_NAME, value="body").get_attribute("innerHTML")
        self.assertEqual(text_on_page, "list of all customers")

    def test_go_to_customer_orders(self):
        customer_id = 1
        self.app.go_to_customer_orders(customer_id)
        text_on_page = self.driver.find_element(by=By.TAG_NAME, value="body").get_attribute("innerHTML")
        self.assertEqual(text_on_page, f"orders from customer no {customer_id}")

    def test_go_to_customer_order_details(self):
        customer_id = 1
        order_id = 2
        self.app.go_to_customer_order_details(customer_id, order_id)
        text_on_page = self.driver.find_element(by=By.TAG_NAME, value="body").get_attribute("innerHTML")
        self.assertEqual(text_on_page, f"order no {order_id} from customer no {customer_id}")


if __name__ == "__main__":
    TestsEdge()
