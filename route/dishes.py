from flask import Flask, request
from flask_restx import Namespace, Resource
from DB import db_connect

Dish = Namespace("Dish")

Dish.route('/register_dish')
class Register(Resource):
    def post(self):
        information = {

        }
    
