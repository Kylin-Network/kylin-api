from flask import Flask,make_response, Response, jsonify, request

from api.oracle_framework import OracleFramework
from api.errors import errors

app = Flask(__name__)
app.register_blueprint(errors)
oracle_framework = OracleFramework()

@app.route("/")
def index():
    return Response("Hello, world!", status=200)


@app.route("/api/prices")
def prices():
    currency_pairs = request.args['currency_pairs']
    prices = oracle_framework.get_prices(currency_pairs)
    return make_response(prices, 200)


@app.route("/health")
def health():
    return Response("OK", status=200)


if __name__ == "__main__":
    app.run()