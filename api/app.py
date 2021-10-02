from flask import Flask, Response
from flask_cors import CORS
from flask_restx import Resource
from api.db.models import db
from api.apis import api
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # configured in docker-compose.yml or on local machine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_ERROR_404_HELP'] = False

api.init_app(app)
db.init_app(app)

@api.route('/health', endpoint='health')
class Health(Resource):
    def get(self):
        return Response("OK", status=200)

if __name__ == "__main__":
    app.run()
