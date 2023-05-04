import unittest

from KawAPI.Webshop.API_Webshop import get_products, get_customers, get_customer_details, get_product_details


class MyTestCase(unittest.TestCase):
    # def test_something(self):
    #     self.assertEqual(True, False)  # add assertion here

    def test_product(self):
        self.assertIsNotNone(get_products, 'Not empty')

    def test_customers(self):
        self.assertIsNotNone(get_customers, 'Not empty')

    def test_product_id(self):
        self.assertIsNotNone(get_product_details(7), 'Not empty')

    def test_customer_id(self):
        self.assertIsNotNone(get_customer_details(7), 'Not empty')

    # def test_product_id_null(self):
    #     self.get_product_details(0)

if __name__ == '__main__':
    unittest.main()
