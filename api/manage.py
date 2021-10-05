from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from functools import wraps
from api.db.models import Users
import os

def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['RESTX_ERROR_404_HELP'] = False
    app.config['RATELIMIT_STORAGE_URL'] = os.getenv('RATELIMIT_STORAGE_URL')
    app.config['RATELIMIT_STRATEGY'] = "fixed-window"
    app.config['RATELIMIT_ENABLED'] = True # if false, rate limits disabled
    return app

# Limiter object used for client rate limits
limiter = Limiter(key_func=lambda: request.headers["x-api-key"], default_limits=["100/minute, 2/second"])

# Localhost is not subjected to rate limits
@limiter.request_filter
def ip_whitelist():
    return request.remote_addr == "127.0.0.1"

# Decorator used to ensure API key is valid
def require_apikey(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Localhost not required to pass an API key
        if request.remote_addr == "127.0.0.1":
            return func(*args, **kwargs)
        if request.headers["x-api-key"]:
            if Users.query.filter_by(api_key=request.headers["x-api-key"]).first():
                return func(*args, **kwargs)
            else:
                raise RuntimeError("API key could not be verified.")
        else:
            raise RuntimeError("Must pass API key with header 'x-api-key'.")
    return decorated_function
