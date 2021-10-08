from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from functools import wraps
from api.db.models import Users
from api.errors.exceptions import InvalidApiKey
import os
import logging

def create_app():
    app = Flask(__name__)
    cors = CORS(app) 
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['RESTX_ERROR_404_HELP'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ratelimit_storage_url = os.getenv('RATELIMIT_STORAGE_URL')
    if ratelimit_storage_url:
        app.config['RATELIMIT_STORAGE_URL'] = ratelimit_storage_url
    else:
        app.config['RATELIMIT_STORAGE_URL'] = "memory://"
        logging.warning(f"Rate limit storage is configured to 'memory://'. This is not suitable for production.")
    app.config['RATELIMIT_STRATEGY'] = "fixed-window"
    app.config['RATELIMIT_ENABLED'] = False # Toggle rate limits on/off
    return app

# Limiter object used for client rate limits
limiter = Limiter(
    # key_func defines how to identify the client
    key_func=lambda: request.headers["x-api-key"] if "x-api-key" in request.headers else get_remote_address(),
    # default rate limits applied to all routes
    default_limits=["1000/minute", "50/second"],
)

# Exclude ip address from being subjected to rate limits
# @limiter.request_filter
# def ip_whitelist():
#     return request.remote_addr == "127.0.0.1"

# Decorator used to ensure API key is valid
def require_apikey(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "x-api-key" in request.headers and Users.query.filter_by(api_key=request.headers["x-api-key"]).first():
                return func(*args, **kwargs)
        else:
            raise InvalidApiKey()
    return decorated_function
