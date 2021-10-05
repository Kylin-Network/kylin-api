from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace
from api.errors.exceptions import InvalidContentType, InvalidSubmitParam, InvalidQueryParam
from api.db.data_store import DataStore
from api.db.models import ParachainData
from api.manage import require_apikey, limiter

parachain_db = Namespace("parachain_db", description="parachain database endpoints")

@parachain_db.route('/submit', endpoint='parachain/submit')
@parachain_db.param('para_id', 'Parachain id which transaction originated from.')
@parachain_db.param('account_id', 'Account id which initiated transaction.')
@parachain_db.param('requested_block_number', 'Requested block number.')
@parachain_db.param('processed_block_number', 'Processed block number.')
@parachain_db.param('requested_timestamp', 'Requested timestamp.')
@parachain_db.param('processed_timestamp', 'Processed timestamp.')
@parachain_db.param('payload', 'JSON serializable data to be stored')
@parachain_db.param('feed_name', 'Feed name which payload is referenced to on-chain.')
@parachain_db.param('url', 'URL which was used to fetch data, if used at all.')
class SubmitData(Resource):
    decorators = [require_apikey, limiter.limit("1/hour")]
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

@parachain_db.route('/query/sql', endpoint='parachain/query/sql')
@parachain_db.param('query', 'SQL query used to query parachina data.')
class QuerySQL(Resource):
    decorators = [require_apikey, limiter.limit("2/hour")]
    def get(self):
        query = request.args["query"]
        results = ParachainData.sql(query)
        return make_response(jsonify(results), 200)

@parachain_db.route('/query/all', endpoint='parachain/query/all')
class QueryAll(Resource):
    decorators = [require_apikey, limiter.limit("3/hour")]
    def get(self):
        results = ParachainData.select_all()
        return make_response(jsonify(results), 200)

@parachain_db.route('/query', endpoint='parachain/query')
@parachain_db.param('hash', "Used to query data related to the hash's feed name.")
@parachain_db.param('feed', 'Used to query data related to the feed name. If both hash and feed are passed, feed is default.')
class QueryFeedOrHash(Resource):
    decorators = [require_apikey, limiter.limit("4/hour")]
    def get(self):
        if "feed" in request.args:
            results = ParachainData.select_all_by_feed(request.args["feed"])
        elif "hash" in request.args:
            results = ParachainData.select_all_by_hash(request.args["hash"])
        else:
            raise InvalidQueryParam(payload=request.args)
        return make_response(jsonify(results), 200)
