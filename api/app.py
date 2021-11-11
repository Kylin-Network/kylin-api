from flask import Flask, make_response, Response, request, jsonify
from flask_cors import CORS
from flask_restx import Resource
from api.oracle_framework import OracleFramework
from api.errors.exceptions import *
from api.db.data_store import DataStore
from api.db.models import db, ParachainDB
from api.api import api
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI') # configured in docker-compose.yml or on local machine
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_ERROR_404_HELP'] = False

api.init_app(app)
db.init_app(app)
oracle_framework = OracleFramework()

@api.route('/health', endpoint='health')
class Health(Resource):
    def get(self):
        return Response("OK", status=200)

@api.route('/prices', endpoint='prices')
@api.param('currency_pairs', 'The currency pairs of which to query price data.')
class Prices(Resource):
    def get(self):
        currency_pairs = request.args['currency_pairs']
        prices = oracle_framework.get_prices(currency_pairs)
        if oracle_framework.has_results(prices):
            return make_response(prices, 200)
        else:
            raise InvalidCurrencyPair(payload=currency_pairs)

@api.route('/submit', endpoint='submit')
@api.param('data', 'JSON data to store.')
class SubmitData(Resource):
    def post(self):
        try:
            body = request.get_json()
            store = DataStore(body)
        except Exception as ex:
            if isinstance(ex, InvalidPayload):
                raise ex
            else:
                raise InvalidSubmitParam(ex)
        ParachainDB.insert_new_row(store)
        return make_response({"message":"Data submitted successfully."}, 200)

@api.route('/query', endpoint='query')
@api.param('hash', "Used to query data related to the hash's feed name.")
class QueryData(Resource):
    def get(self):
        if "hash" in request.args:
            results = ParachainDB.select_all_by_hash(request.args["hash"])
        else:
            raise InvalidQueryParam(payload=request.args)
        return make_response(jsonify(results), 200)

@api.route('/query/all', endpoint='query/all')
class QueryAll(Resource):
    def get(self):
        results = ParachainDB.select_all()
        return make_response(jsonify(results), 200)

if __name__ == "__main__":
    app.run()
