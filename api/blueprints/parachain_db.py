from flask import make_response, request, jsonify
from flask_restx import Resource, Namespace
from api.errors.exceptions import InvalidContentType, InvalidSubmitParam, InvalidQueryParam
from api.db.data_store import DataStore
from api.db.models import ParachainData
from api.manage import require_apikey, limiter

parachain_db = Namespace("parachain_db", description="Parachain database endpoints.")

@parachain_db.route('/query', endpoint='parachain/query')
@parachain_db.param('feed', 'On-chain feed name to query for.')
class QueryData(Resource):
    # decorators = [require_apikey, limiter.limit("10/second")]
    def get(self):
        if "feed" in request.args:
            results = ParachainData.select_all_by_feed(request.args["feed"])
        else:
            raise InvalidQueryParam(payload=request.args)
        return make_response(jsonify(results), 200)

@parachain_db.route('/submit', endpoint='parachain/submit')
@parachain_db.param('para_id', 'Parachain id which transaction originated from.')
@parachain_db.param('account_id', 'Account id which initiated transaction.')
@parachain_db.param('requested_block_number', 'Requested block number.')
@parachain_db.param('processed_block_number', 'Processed block number.')
@parachain_db.param('requested_timestamp', 'Requested timestamp in milliseconds.')
@parachain_db.param('processed_timestamp', 'Processed timestamp in milliseconds.')
@parachain_db.param('payload', 'JSON serializable data to be stored')
@parachain_db.param('feed_name', 'Feed name which payload is referenced to on-chain.')
@parachain_db.param('url', 'URL which was used to fetch data, if used at all.')
class SubmitData(Resource):
    # decorators = [require_apikey, limiter.limit("10/second")]
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
