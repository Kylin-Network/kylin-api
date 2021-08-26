from flask_restx import Api
from api.errors.error_handler import errors

api = Api(
    doc='/swagger',
    version='1.0.0',
    title='kylin-api',
    description="Kylin Network's API providing price feed data from various sources (bancor, coinbase, coingecko, cryptocompare, cryptowatch, etc)",
)
api.add_namespace(errors)
