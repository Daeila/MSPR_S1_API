#Installer Flask en utilisant la commande pip:
#pip install flask

from flask import Flask, jsonify
import requests
import json

app = Flask(__name__)

# Créer un endpoint pour récupérer tous les produits
@app.route('/api/v1/products', methods=['GET'])
def get_products():
    products = requests.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products')
    p = jsonify(products.json())
    return p

# Créer un endpoint pour récupérer tous les customers
@app.route('/api/v1/customers', methods=['GET'])
def get_customers():
    products = requests.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers')
    c = jsonify(products.json())
    return c

import requests as r
def get_product_details(product_id):
    try:
      response = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}")
      return response.json()
    except:
      return "un msg d'erreur ou un truc dans le genre jsp"

#result = get_product_details(3)
#print(result)

def get_customer_details(customerId):
    try:
      response = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{customerId}")
      return response.json()
    except:
      return "un msg d'erreur ou un truc dans le genre jsp"

#result = get_customer_details(7)
#print(result)



if __name__ == '__main__':
    app.run(debug=True)
