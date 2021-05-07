from flask import Flask
from flask_restx import Resource, Api
from route import users
from DB import db_connect
app = Flask(__name__)
api = Api(app)

api.add_namespace(users.User, "/auth")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db_connect.Db_coneection()
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
