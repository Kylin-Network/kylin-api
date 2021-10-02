from flask_restx import Api
from api.errors.error_handler import errors
from api.apis.database import database
from api.apis.prices import prices

api = Api(
    doc='/',
    version='1.0.0',
    title='Kylin API',
    description="Kylin Network's API providing price feed data from various sources (bancor, coinbase, coingecko, cryptocompare, cryptowatch, etc) and other functionality.",
)

api.add_namespace(errors)
api.add_namespace(prices, path="/prices")
api.add_namespace(database, path='/database')
