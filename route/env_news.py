from flask import Flask, request
from flask_restx import Namespace, Resource
from DB import db_connect
from ibmcloudant.cloudant_v1 import AllDocsQuery, Document, CloudantV1

Dish = Namespace("Dish")
Dish.route('/register_dish')
import uuid
service = db_connect.Db_coneection().get_service()

News = Namespace('News')
@News.route("post")
class Post(Resource):
    def post(self):
        information = {
            "title": request.args.json('title'),
            "content": request.args.json('content'),
            "writer": request.args.json('writer'),
            "date": request.args.json('date')
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            products_doc = Document(
                id=f"cfc:{uuid.uuid1()}",
                title=information["title"],
                content=information['content'],
                writer=information['writer'],
                date=information['date']
            )
            response = service.post_document(db='env_news', document=products_doc).get_result()

            return {"message": "success"}, 200
        except Exception as e:
            return {"message": "Internal server error"}, 500

    def get(self):
        information = {
            "shop_id": request.args.get('shop_id')
        }

