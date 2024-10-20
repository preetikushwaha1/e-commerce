from flask import Flask , request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy(app)


#create Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False) 
    
    def __repr__(self):
        return f"title: {self.title}"

    
with app.app_context():
    db.create_all()
  
  
    

#create new products
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    print(data)
    if 'title' not in data or 'price' not in data or 'category' not in data:
        abort(400, description="missing 'title' or 'price' or 'category' ")
        
    new_product = Product(
        title = data['title'],
        description = data['description'],
        category = data['category'],
        price = data['price']
        )
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'id':new_product.id,
                    'title':new_product.title,
                    'description': new_product.description,
                    'category': new_product.category,
                    'price':new_product.price}), 201




#get all the products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    products_data =[]
    if products:
        for product in products:
            products_data.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'category': product.category,
                'price': product.price
            })
        
        return jsonify(products_data), 200
    else:
        return jsonify({"message": "Product not found"}), 404




#get specific product 
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    return jsonify({
        'id': product.id,
        'title': product.title,
        'description': product.description,
        'category': product.category,
        'price': product.price
        }), 200




#update specific product 
@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    data = request.get_json()
    product.title = data['title']
    product.description = data['description']
    product.category = data['category']
    product.price = data['price']
    
    db.session.commit()
    
    return jsonify({'title':product.title,
                    'description': product.description,
                    'category': product.category,
                    'price': product.price}), 200




#delete specific product 
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({"message": "Product deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)