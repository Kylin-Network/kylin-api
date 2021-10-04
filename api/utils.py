from functools import wraps
from api.db.models import Users
from flask import request
from flask_limiter import Limiter

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
        # Localhost is not required to pass an API key
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
