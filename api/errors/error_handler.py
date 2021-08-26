from flask_restx import Namespace
from api.errors.exceptions import *

errors = Namespace("errors", description="error handler")

@errors.errorhandler(InvalidQuery)
def invalid_query_error(error):
    return {"message":f"No results found for '{error.payload}'. {error.message}."}, 400

@errors.errorhandler(Exception)
def server_error(error):
    return {"message": f"Oops, got an error! {error}"}, 500
