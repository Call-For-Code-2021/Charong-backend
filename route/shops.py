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
            'dish_type': request.json.get('dish_type')
        }
        for i in information:
            if information[i] is None:
                return {'message': "Bad request"}, 400
        try:
            products_doc = Document(
                id=f"cfc:{uuid.uuid1()}",
                shop=information['shop_name'],
                shop_num=information['shop_num'],
                user_id=information['user_id'],
                address=information['address'],
                dish_type=information['dish_type']
            )
            service.post_document(db='shops', document=products_doc).get_result()
            # service.put_document(db='users', doc_id=f"cfc:{information['user_id']}", document=user_doc).get_result()

            return {'message': "OK"}, 200
        except Exception as e:
            print(e)
            return {'message': "Internal Server Error"}, 500

    def get(self):
        '''
        shop 검색       :return:
        '''
        information = {
            "shop_id": request.args.get("shop_id")
        }
        if information['id'] is None:
            return {'message': "Bad request"}, 400
        try:
            response = service.post_find(db='shops', selector={
                '_id': {
                    '$eq': f"cfc:{information['id']}"
                }
            }).get_result()
            rating = service.post_find(db='ratings', selector={
                'shop_id': {
                    '$eq': information['shop_id']
                    }
                }).get_result()


            if response['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404

            if rating['bookmark'] == 'nil':
                response['docs'][0]['rating'] = None

            else:
                #평점 계산하기 위한 변수
                count = 0
                # 평점 갯수 카운트 하기 위한 변수
                c = 0
                for score in rating['docs']:
                    count += score['rating']
                    c += 1
                avg_rating = count / c
                response['docs'][0]['rating'] = avg_rating
            return response['docs'][0], 200
        except Exception as e:
            return {'message': 'Internal Server Error'}, 500




@Shops.route('/map')
class Map(Resource):
    def post(self):
        information = {
            'shop_id': request.json.get('shop_id'),
            'user_id': request.json.get('user_id')
        }
        try:
            response = service.post_find(db='shops', selector={
                '$and': [
                    {
                        "x": {
                            "$gte": 300
                        },
                        "x": {
                            "$lte": 1000
                        }
                    }
                ]
            }).get_result()
            print(response)
        except Exception as e:

            print(e)

    def get(self):
        information = {
            'x1': request.args.get('x1'),
            'x2': request.args.get('x2'),
            'y1': request.args.get('y1'),
            'y2': request.args.get('y2'),
            'from': request.args.get('from'),
            'limit': request.args.get("limit")
        }
        for i in information:
            if information[i] is None:
                return {'message': "Bad request"}, 400

        try:
            print(information)
            response = service.post_find(db='shops', selector={
                '$and': [
                    {
                        'x': {'$gte': int(information['x1'])}

                    },
                    {
                        'x': {'$lte': int(information['x2'])}
                    },
                    {
                        'y': {'$gte': int(information['y1'])}

                    },
                    {
                        'y': {'$lte': int(information['y2'])}
                    }
                ]
            }, skip=information['from'], limit=information['limit']).get_result()
            print(response)

            if response['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404
            data = {}
            for i in response['docs']:
                data[i['_id']] = i
            return data, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

        # return response['docs'][0], 200


@Shops.route('/rating')
class Rating(Resource):
    def post(self):
        information = {
            'shop_id': request.json.get('shop_id'),
            'user_id': request.json.get('user_id'),
            'rating': request.json.get('rating')
        }
        for i in information:
            if information[i] is None:
                return {'message': 'Bad request'}, 400
        try:
            products_doc = Document(
                id=f"cfc:{uuid.uuid1()}",
                shop_id=information['shop_id'],
                user_id=information['user_id'],
                rating=information['rating']
            )
            service.post_document(db='ratings', document=products_doc).get_result()
            return {'message': 'success'}
        except Exception:
            return {'message': "Internal Server Error"}
@Shops.route('/list')
class ShopList(Resource):
    def get(self):
        information = {
            'from': request.args.get('from'),
            'limit': request.args.get('limit')
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            shops = service.post_find(db='shops', selector={
                "_id": {
                    "$ne": "cfc"
                }
            }, limit=int(information['limit']), skip=int(information['from'])).get_result()


            print(shops)
            if shops['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404
            send_data = {}  # 가공된 데이터를 담을 dictionary
            for i in shops['docs']:
                send_data[i['_id']] = i
            return send_data, 200
        except Exception as e:
            print(e)
            return {"message": "Internal server error"}, 500