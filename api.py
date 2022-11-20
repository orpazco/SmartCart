from flask import Flask, jsonify
from flask import request
from db import db_session as db

app = Flask(__name__)


@app.route('/addCustomer', methods=['POST'])
def add_new_customer():
    try:
        cid = request.json.get('cid')
        name = request.json.get('name')
        db.add_new_customer(cid, name, True)
        return f'add customer {id} successfully'
    except Exception as e:
        return e.args[0], 400


@app.route('/addItemToCart/<string:item_id>', methods=['POST'])
def add_item_to_cart(item_id):
    try:
        cid = request.json.get('cid')
        db.add_item_to_cart(cid, item_id)
        return "Success"
    except Exception as e:
        return e.__cause__, 400


@app.route('/getCart/<int:customer_id>', methods=['GET'])
def get_cart(customer_id):
    try:
        cart = db.get_cart(customer_id)
        return jsonify(cart)
    except Exception as e:
        return e.__cause__, 400

