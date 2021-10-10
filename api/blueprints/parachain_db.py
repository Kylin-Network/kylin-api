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
@parachain_db.param('data', 'JSON data to store.')
class SubmitData(Resource):
    # decorators = [require_apikey, limiter.limit("10/second")]
    def post(self):
        if not request.is_json:
            raise InvalidContentType(payload=request.content_type)
        try:
            body = request.get_json()
            store = DataStore(**body)
        except:
            raise InvalidSubmitParam()
        ParachainData.insert_new_row(store)
        return make_response({"message":"Data submitted successfully."}, 200)
