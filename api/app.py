from flask import make_response, Response, request
from flask_restx import Resource
from api.oracle_framework import OracleFramework
from api.restx import api, app
from api.errors import InvalidCurrencyPair

oracle_framework = OracleFramework()

@api.route('/prices', endpoint='prices')
@api.param('currency_pairs', 'the currency_pairs')
class PriceList(Resource):
    def get(self):
        currency_pairs = request.args['currency_pairs']
        prices = oracle_framework.get_prices(currency_pairs)
        if oracle_framework.has_results(prices):
            return make_response(prices, 200)
        else:
            raise InvalidCurrencyPair

@api.route('/health', endpoint='health')
class HealthList(Resource):
    def get(self):
        return Response("OK", status=200)


if __name__ == "__main__":
    app.run()
