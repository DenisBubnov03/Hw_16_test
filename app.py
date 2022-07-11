from flask import Flask, jsonify, request
import json

from file.SQLalchemy import db
from file.DataBase import DataBase
from file.Models import User, Order, Offer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)
app.app_context().push()

db.create_all()

DataBase().load_all_users()
DataBase().load_all_order()
DataBase().load_all_offer()


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/users/', methods=['GET', 'POST'])
def all_users_page():
    if request.method == 'GET':
        users_list = []
        for user in User.query.all():
            users_list.append(user.get_dict())

        return jsonify(users_list)
    elif request.method == 'POST':
        user_info = json.loads(request.data)
        DataBase().add_user(user_info)
        return ""


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def users_by_id_page(pk):
    if request.method == 'GET':
        user = User.query.get(pk)
        if user:
            return jsonify(user.get_dict())
        return jsonify([])
    elif request.method == 'PUT':
        user_info = json.loads(request.data)
        DataBase().update_user(pk, user_info)
        return ""
    elif request.method == "DELETE":
        DataBase().delete_user(pk)
        return ""


@app.route('/orders/', methods=['GET', 'POST'])
def all_orders_page():
    if request.method == 'GET':
        orders_list = []
        for order in Order.query.all():
            orders_list.append(order.get_dict())

        return jsonify(orders_list)
    elif request.method == 'POST':
        order_info = json.loads(request.data)
        DataBase().add_order(order_info)
        return ""


@app.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def orders_by_id_page(pk):
    if request.method == 'GET':
        order = Order.query.get(pk)
        if order:
            return jsonify(order.get_dict())
        return jsonify([])
    elif request.method == 'PUT':
        order_info = json.loads(request.data)
        DataBase().update_order(pk, order_info)
        return ""
    elif request.method == "DELETE":
        order = Order.query.get(pk)
        db.session.delete(order)
        db.session.commit()
        return "", 200


@app.route('/offers/', methods=['GET', 'POST'])
def all_offers_page():
    if request.method == 'GET':
        offers_list = []
        for offer in Offer.query.all():
            offers_list.append(Offer.get_dict(offer))

        return jsonify(offers_list)
    elif request.method == 'POST':
        offer_info = json.loads(request.data)
        DataBase().add_offer(offer_info)
        return ""


@app.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def offers_by_id_page(pk):
    if request.method == 'GET':
        offer = Offer.query.get(pk)
        if offer:
            return jsonify(offer.get_dict())
        return jsonify([])
    elif request.method == 'PUT':
        offer_info = json.loads(request.data)
        DataBase().update_offer(pk, offer_info)
        return ""
    elif request.method == "DELETE":
        DataBase().delete_offer(pk)
        return ""


if __name__ == '__main__':
    app.run()
