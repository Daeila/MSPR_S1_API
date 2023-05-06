
from flask import Flask, jsonify
import requests as r

app = Flask(__name__)


@app.route('/api/v1/products', methods=['GET'])
def get_products():
    products = r.get('https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products')
    c = jsonify(products.json())
    return c

@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    try:                            
      response = r.get(f"https://615f5fb4f7254d0017068109.mockapi.io/api/v1/products/{product_id}")
      return response.json()
    except:
      return "un msg d'erreur ou un truc dans le genre jsp"
      result = get_product_details(5)

    print(result)


if __name__== '__main__':
    app.run(debug=True)
