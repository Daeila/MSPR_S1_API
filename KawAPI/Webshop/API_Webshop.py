#Installer Flask en utilisant la commande pip:
#pip install flask

from flask import Flask, jsonify

app = Flask(__name__)

# Créer un endpoint pour récupérer tous les produits
@app.route('/api/products', methods=['GET'])
def get_products():
    products = [
        {'id': 1, 'name': 'Produit 1', 'price': 10.99},
        {'id': 2, 'name': 'Produit 2', 'price': 19.99},
        {'id': 3, 'name': 'Produit 3', 'price': 7.99},
    ]
    return jsonify(products)

# Créer un endpoint pour récupérer un produit par ID
@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    products = [
        {'id': 1, 'name': 'Produit 1', 'price': 10.99},
        {'id': 2, 'name': 'Produit 2', 'price': 19.99},
        {'id': 3, 'name': 'Produit 3', 'price': 7.99},
    ]
    for product in products:
        if product['id'] == id:
            return jsonify(product)
    return jsonify({'message': 'Produit non trouvé'})

if __name__ == '__main__':
    app.run(debug=True)
