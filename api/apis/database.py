from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace
from api.errors.exceptions import InvalidContentType, InvalidSubmitParam, InvalidQueryParam
from api.db.data_store import DataStore
from api.db.models import ParachainData

database = Namespace("database", description="database api endpoints")

@database.route('/submit', endpoint='submit')
@database.param('data', 'JSON data to store.')
@database.param('hash', 'Hash of data written on-chain.')
@database.param('feed', 'Feed name of which hash is referenced to on-chain.')
@database.param('block', 'Block number which hash is written to.')
class SubmitData(Resource):
    def post(self):
        if not request.is_json:
            raise InvalidContentType(payload=request.content_type)
        try:
            kwargs = request.get_json()
            store = DataStore(**kwargs)
        except:
            raise InvalidSubmitParam()
        ParachainData.insert_new_row(store)
        return make_response({"message":"Data submitted successfully."}, 200)

@database.route('/query/sql', endpoint='query/sql')
@database.param('query', 'SQL query used to query parachina data.')
class QuerySQL(Resource):
    def get(self):
        query = request.args["query"]
        results = ParachainData.sql(query)
        return make_response(jsonify(results), 200)

@database.route('/query/all', endpoint='query/all')
class QueryAll(Resource):
    def get(self):
        results = ParachainData.select_all()
        return make_response(jsonify(results), 200)

@database.route('/query', endpoint='query')
@database.param('hash', "Used to query data related to the hash's feed name.")
@database.param('feed', 'Used to query data related to the feed name. If both hash and feed are passed, feed is default.')
class QueryFeedOrHash(Resource):
    def get(self):
        if "feed" in request.args:
            results = ParachainData.select_all_by_feed(request.args["feed"])
        elif "hash" in request.args:
            results = ParachainData.select_all_by_hash(request.args["hash"])
        else:
            raise InvalidQueryParam(payload=request.args)
        return make_response(jsonify(results), 200)
