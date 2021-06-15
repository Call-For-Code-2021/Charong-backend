from flask import Flask, request
from flask_restx import Namespace, Resource
from DB import db_connect
from ibmcloudant.cloudant_v1 import AllDocsQuery, Document, CloudantV1

Dish = Namespace("Dish")
Dish.route('/register_dish')
import uuid
service = db_connect.Db_coneection().get_service()

News = Namespace('News')
@News.route("/get_all")
class List(Resource):
    def get(self):
        '''
        뉴스기사 리스트별로 가져오기
        '''
        information = {
            'from': request.args.get('from'),
            'limit': request.args.get('limit')
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            news = service.post_find(db='env_news', selector={
                        "_id": {
                            "$ne": "cfc"
                        }
            }, limit=int(information['limit']), skip=int(information['from'])).get_result()
            query = AllDocsQuery(
                limit=int(information['limit']),
                skip=int(information['from'])

            )
            # news = service.post_all_docs_queries(db="env_news", queries=[query]).get_result()
            # news = service.post_design_docs_queries(
            #     db='env_news',
            #     queries=[query]
            # ).get_result()
            print(news)
            if news['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404
            send_data = {} # 가공된 데이터를 담을 dictionary
            for i in news['docs']:
                send_data[i['_id']] = i
            return send_data, 200
        except Exception as e:
            print(e)
            return {"message": "Internal server error"}, 500
@News.route("post")
class Post(Resource):
    def post(self):
        '''
        뉴스 포스트하기
        '''
        information = {
            "title": request.json.get('title'),
            "content": request.json.get('content'),
            "writer": request.json.get('writer'),
            "date": request.json.get('date')
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
        '''
        뉴스 가져오기
        :return:
        '''
        information = {
            "id": request.args.get('id')
        }
        if information['id'] is None:
            return {"message": "Bad request"}, 400
        try:
            news_detail = service.post_find(db='env_news', selector={
                '_id': {
                    '$eq': information['shop_id']
             }
            }).get_result()

            if news_detail['bookmark'] == 'nil':
                return {'message': 'Data not found'}, 404
            return {"news_id": information['id'],"title": news_detail['docs'][0]['title'], "content": news_detail['docs'][0]['content'], "writer": news_detail['docs'][0]['writer'], "date": news_detail['docs'][0]['date']}, 200
        except Exception as e:
            return {"message": "Internal server error"}, 500