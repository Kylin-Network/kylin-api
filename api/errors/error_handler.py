from flask_restx import Namespace
from api.errors.exceptions import *

errors = Namespace("errors", description="error handler")

@errors.errorhandler(InvalidCurrencyPair)
def invalid_currency_error(error):
    return {"message": f"No results found for '{error.payload}'. Use valid currency symbols with format: '<FROM-CURRENCY>_<TO-CURRENCY>'. If passing multiple currency pairs, separate them with commas. Example: btc_usd,eth_gbp,kyl_jpy"}, 404

@errors.errorhandler(InvalidContentType)
def invalid_content_type_error(error):
    return {"message": f"Content type of '{error.payload}' is not valid. Use 'content-type: application/json' in your header and pass valid json format."}, 400

@errors.errorhandler(InvalidQueryParam)
def invalid_query_param_error(error):
    return {"message": f"'{error.payload}' is not a valid parameter. Pass feed name to query data for."}, 400

@errors.errorhandler(InvalidSubmitParam)
def invalid_submit_param_error(error):
    return {"message": f"Submit did not succeed. Pass valid json format with the following keys: 'para_id', 'account_id', 'requested_block_number', 'processed_block_number', 'requested_timestamp', 'processed_timestamp', 'payload', 'feed_name', 'url'."}, 400

@errors.errorhandler(InvalidApiKey)
def invalid_api_key(error):
    return {"message": f"Authentication failed. Pass a valid API key with header 'x-api-key: YOUR_API_KEY'."}, 401

@errors.errorhandler(ExistingUserFound)
def existing_user_found(error):
    return {"message": f"Existing API key found for '{error.payload}'. Only one API key per account is allowed."}, 422

@errors.errorhandler(Exception)
def server_error(error):
    return {"message": f"Oops, got an error! {error}"}, 500
