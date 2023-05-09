import unittest
import requests
from unittest.mock import patch
from api2 import app

class TestProductDetails(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_product_details_success(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {"id": 5, "name": "Jacquelyn Hyatt"}
            response = self.app.get('/api/v1/products/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"id": 5, "name": "Jacquelyn Hyatt"})

    def test_get_product_details_error(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = Exception("mock error message")
            response = self.app.get('/api/v1/products/5')
            self.assertEqual(response.status_code, 500)  # Le code de réponse HTTP doit être 200 même en cas d'erreur
            self.assertEqual(response.json, None)  # La réponse JSON attendue est None

if __name__ == '__main__':
     unittest.main()