from flask_restx import Api
from flask import Flask
from api.errors import InvalidCurrencyPair

app = Flask(__name__)
api = Api(
    app,
    doc='/swagger',
    version='1.0.0',
    title='kylin-api',
    description='The API to provide the price feeds for the currency pairs from different sources(coingecko, coinbase, kraken, cryptowatch, etc)',
)

@api.errorhandler(InvalidCurrencyPair)
def invalid_currency_pairs_error(error):
    return {"message":f"InvalidCurrencyPair: {error}"}, 400

@api.errorhandler(Exception)
def server_error(error):
    return {"message": f"Oops, got an error! {error}"}, 500