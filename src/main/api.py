from collections import Counter

from flask import Flask
from flask import request

from db import db_session as db

app = Flask(__name__)
PRODUCT_NAME = 0
COST = 1


@app.route('/addCustomer', methods=['POST'])
def add_new_customer():
    try:
        cid = request.json.get('cid')
        name = request.json.get('name')
        db.add_new_customer(cid, name)
        return f'add customer {name}: {cid} successfully'
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
        return Counter([p[PRODUCT_NAME] for p in cart])
    except Exception as e:
        return e.__cause__, 400


@app.route('/getTotal/<int:customer_id>', methods=['GET'])
def get_total(customer_id):
    try:
        cart = db.get_cart(customer_id)
        prod_list = [p[COST] for p in cart]
        return {"cart": Counter([p[PRODUCT_NAME] for p in cart]),
                "total": round(sum(prod_list), 3)}
    except Exception as e:
        return e.__cause__, 400
