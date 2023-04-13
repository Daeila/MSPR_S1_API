import requests as r
from flask import jsonify

response = r.get("http://localhost:5000/products/1", headers={"API_KEY": "test"})

print(response.status_code)
print(response.text)
