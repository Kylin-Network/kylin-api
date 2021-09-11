from flask import Flask, make_response, Response, request, jsonify
from flask_cors import CORS
from flask_restx import Resource
from api.oracle_framework import OracleFramework
from api.errors.exceptions import *
from api.config import CONN_STRING
from api.db.data_store import DataStore
from api.db.models import db, ParachainDB
from api.api import api

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = CONN_STRING
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
@api.param('hash', 'Hash of data written on-chain.')
@api.param('feed', 'Feed name of which hash is referenced to on-chain.')
@api.param('block', 'Block number which hash is written to.')
class SubmitData(Resource):
    def post(self):
        if not request.is_json:
            raise InvalidContentType(payload=request.content_type)
        try:
            kwargs = request.get_json()
            store = DataStore(**kwargs)
        except:
            raise InvalidSubmitParam()
        ParachainDB.insert_new_row(store)
        return make_response({"message":"Data submitted successfully."}, 200)

@api.route('/query', endpoint='query')
@api.param('hash', "Used to query data related to the hash's feed name.")
@api.param('feed', 'Used to query data related to the feed name. If both hash and feed are passed, feed is default.')
class QueryData(Resource):
    def get(self):
        if "feed" in request.args:
            results = ParachainDB.select_all_by_feed(request.args["feed"])
        elif "hash" in request.args:
            results = ParachainDB.select_all_by_hash(request.args["hash"])
        else:
            raise InvalidQueryParam(payload=request.args)
        return make_response(jsonify(results), 200)

if __name__ == "__main__":
    app.run()
