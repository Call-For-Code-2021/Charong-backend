from flask import Flask, request
from flask_restx import Namespace, Resource
from DB import db_connect

Dish = Namespace("Dish")

Dish.route('/register_dish')
class RegisterDishes(Resource):
    def post(self):
        information = {

        }

    def get(self):
        information = {
            "shop_id": request.args.get('shop_id')
        }

