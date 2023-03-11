from flask import Flask, jsonify, abort
from flask_cors import CORS
from models import Product, ProductUser
from models import db
import requests

from producer import publish

app = Flask(__name__)
with app.app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)


    @app.before_first_request
    def create_table():
        db.create_all()


    @app.route('/api/products')
    def index():  # put application's code here
        return jsonify(Product.query.all())


    @app.route('/api/products/<int:id>/like', methods=['POST'])
    def like(id):
        req = requests.get("http://host.docker.internal:8000/api/user")
        json = req.json()

        try:
            productUser = ProductUser(user_id=json['id'], product_id=id)
            db.session.add(productUser)
            db.session.commit()

            # send event
            publish('product_liked',id)
        except:
            abort(400, 'You already liked this product')
        return jsonify({
            'message': 'success'
        })


    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')
