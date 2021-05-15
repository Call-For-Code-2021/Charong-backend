import ibm_cloud_sdk_core
from flask import Flask, request
from flask_restx import Namespace, Resource
from DB import db_connect
from ibmcloudant.cloudant_v1 import AllDocsQuery, Document, CloudantV1
import uuid

Shops = Namespace('Shop')
service = db_connect.Db_coneection().get_service()


@Shops.route('/shop')
class Shop(Resource):
    def post(self):
        information = {
            'shop_name': request.json.get('shop_name'),
            'address': request.json.get('address'),
            'shop_num': request.json.get('shop_num'),
            'user_id': request.json.get('user_id'),
            'x': request.json.get('x'),
            'y': request.json.get('y')
        }
        for i in information:
            if information[i] is None:
                return {'message': "Bad request"}, 400
        try:
            products_doc = Document(
                id=uuid.uuid1(),
                shop=information['shop_name'],
                shop_num=information['shop_num'],
                user_id=information['user_id'],
                x=information['x'],
                y=information['y']
            )

            service.post_document(db='shops', document=products_doc).get_result()
            return {'message': "OK"}, 200
        except Exception:
            return {'message': "Internal Server Error"}, 500

    def get(self):
        information = {
            id: request.args.get("id")
        }
        if information['id'] is None:
            return {'message': "Bad request"}, 400
        try:
            response = service.post_find(db='shops', selector={
                    '_id': {
                        '$eq': information['id']
                    }
                }
            ).get_result()
            if response['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500

        return response['docs'][0], 200
@Shops.route('/map')
class Map(Resource):

    def get(self):
        information = {
            'x1': request.args.get('x1'),
            'x2': request.args.get('x2'),
            'y1': request.args.get('y1'),
            'y2': request.args.get('y2')
        }
        for i in information:
            if information[i] is None:
                return {'message': "Bad request"}, 400
        
        try:
            response = service.post_find(db='shops', selector={
                '$and': [
                    {
                        'x1': {'$gte': int(information['x1']) }

                    },
                    {
                        'x2': {'$lte': int(information['x2'])}
                    },
                    {
                        'y1': {'$gte': int(information['x1'])}

                    },
                    {
                        'y2': {'$lte': int(information['x2'])}
                    }
                ]
            }).get_result()
            if response['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500

        return response['docs'][0], 200