import ibm_cloud_sdk_core
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, Namespace
import bcrypt
import json
from flask import make_response
from DB import db_connect
from ibmcloudant.cloudant_v1 import AllDocsQuery, Document, CloudantV1
import re
import jwt
import datetime
User = Namespace("User")

service = db_connect.Db_coneection().get_service()


@User.route('/login')
class Login(Resource):
    def post(self): #login function
        information = {
            "id": request.json.get("id"),
            "password": request.json.get("password")
        }

        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            #db 조회
            response = service.get_document(
                db='users',
                doc_id=f"cfc:{information['id']}"
            ).get_result()
            # pw 검증
            if bcrypt.checkpw(information['password'].encode('utf-8'), response['password'].encode('utf-8')) is True:
                jwt_token = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),'id': information['id']}, "qwer@1234", 'HS256')
                return {"jwt_token": jwt_token}, 200
            else:
                return {"messsage": "Unauthorized"}, 401
        except Exception as e:
            return {"message": " Internal Server Error"}, 500

    def get(self): #jwt 에러 찾기
        information = {
            "jwt_token": request.args.get("jwt_token")
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            decoded = jwt.decode(information["jwt_token"], "qwer@1234", 'HS256')
            decoded["jwt_token"] = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),'id': decoded['id']}, "qwer@1234", 'HS256')
            return decoded, 200
        except jwt.ExpiredSignatureError:
            return {"message": "Unathorized"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Unauthorized"}, 401
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500

@User.route('/join')
class Join(Resource):
    '''
    joining system
    '''
    def get(self):
        information = {
            "id": request.args.get('id')
        }
        print(information)
        if information['id'] is None:
            return {"message": "Bad request"}
        try:
            response = service.get_document(db='users', doc_id=f"cfc:{information['id']}")
        except ibm_cloud_sdk_core.api_exception.ApiException as ibm:
            return {"message": "Okay"}, 200
        except Exception as e:
            return {"message": "Internal Server Error"}, 500
        return {"message": "Unauthorized"}, 401

    def post(self):
        # body datas
        information = {
            "id": request.json.get('id'),
            "password": request.json.get('password'),
            "name": request.json.get('name'),
            "address": request.json.get('address')
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400

        password_re = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        id_re = re.compile(r'^[a-z0-9]{4,20}$')

        if password_re.match(information['password']) is None:
            '''
            cheking Regular expressio of password
            '''
            return {"message": "Bad request"}, 400

        if id_re.match(information['id']) is None:
            return {"message": "Bad request"}, 400

        try:
            # encoding password
            hash_password = bcrypt.hashpw(information['password'].encode('utf-8'), bcrypt.gensalt())
            # insert into cloudant db
            products_doc = Document(
                id=f"cfc:{information['id']}",
                password=hash_password.decode('utf-8'),
                name=information['name'],
                address=information['address'],
                type="normal"
            )
            response = service.post_document(db='users', document=products_doc).get_result()
        except Exception as e:
            print(e)
            return {"message": "Internal Server Error"}, 500
        return response, 200

@User.route("/delete")
class Delete(Resource):
    def post(self):
        information = {
            "id": request.json.get("id"),
            "password": request.json.get("password")
        }
        for i in information:
            if information[i] is None:
                return {"message": "Bad request"}, 400
        try:
            response = service.get_document(db='users', doc_id=f"cfc:{information['id']}").get_result()
        except ibm_cloud_sdk_core.api_exception.ApiException as ibm:
            return {"message": "Unauthorized"}, 401
        if bcrypt.checkpw(information['password'].encode("utf-8"), response["password"].encode("utf-8")):
            try:
                response = service.delete_document(
                    db='users',
                    doc_id=f'cfc:{information["id"]}',
                    rev=response['_rev']
                ).get_result()
                return response, 200
            except Exception as e:
                print(e)
                return {"message": "Internal Server Error"}, 500
        else:
            return {"password": "Unauthorize"}, 401
