from flask import make_response, request
from flask_restx import Resource, Namespace
from api.errors.exceptions import InvalidCurrencyPair
from api.oracle_framework import OracleFramework

prices = Namespace("prices", description="price api endpoints")

oracle_framework = OracleFramework()

@prices.route('/market', endpoint='prices')
@prices.param('currency_pairs', 'The currency pairs of which to query price data.')
class Prices(Resource):
    def get(self):
        currency_pairs = request.args['currency_pairs']
        prices = oracle_framework.get_prices(currency_pairs)
        if oracle_framework.has_results(prices):
            return make_response(prices, 200)
        else:
            raise InvalidCurrencyPair(payload=currency_pairs)