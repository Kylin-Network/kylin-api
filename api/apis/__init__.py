from flask import request
from flask_restx import Api
from api.errors.error_handler import errors
from api.apis.parachain_db import parachain_db
from api.apis.price_oracle import prices
from api.apis.auth import auth

api = Api(
    doc='/',
    version='1.0.0',
    title='Kylin API',
    description="Kylin Network's API providing price feed data from various sources (bancor, coinbase, coingecko, cryptocompare, cryptowatch, etc) and other functionality.",
)
api.add_namespace(errors)
api.add_namespace(prices, path="/prices")
api.add_namespace(parachain_db, path='/database')
api.add_namespace(auth, path="/auth")
