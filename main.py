from flask import Flask
from flask_restx import Resource, Api
from route import shops, users, env_news
from DB import db_connect
import os
from flask_cors import CORS, cross_origin


app = Flask(__name__)
api = Api(app)
CORS(app)
api.add_namespace(shops.Shops, "/buy")
api.add_namespace(users.User, "/auth")
api.add_namespace(env_news.News, '/news')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db_connect.Db_coneection()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True, port=os.environ.get('PORT'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
