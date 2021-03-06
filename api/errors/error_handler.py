from flask_restx import Namespace
from api.errors.exceptions import *

errors = Namespace("errors", description="error handler")

@errors.errorhandler(InvalidCurrencyPair)
def invalid_currency_error(error):
    return {"message": f"No results found for '{error.payload}'. Use valid currency symbols with format: '<FROM-CURRENCY>_<TO-CURRENCY>'. If passing multiple currency pairs, separate them with commas. Example: btc_usd,eth_gbp,kyl_jpy"}, error.status_code

@errors.errorhandler(InvalidContentType)
def invalid_content_type_error(error):
    return {"message": f"Content type of '{error.payload}' is not valid. Use 'content-type: application/json' in your header and pass valid json format"}, error.status_code

@errors.errorhandler(InvalidQueryParam)
def invalid_query_param_error(error):
    return {"message": f"'{error.payload}' is not a valid parameter. Pass 'hash' or 'feed' to query data for. If both are passed, 'feed' is used as default"}, error.status_code

@errors.errorhandler(InvalidSubmitParam)
def invalid_submit_param_error(error):
    return {"message": f"Submit did not succeed. Pass valid json format with the required keys and types"}, error.status_code

@errors.errorhandler(InvalidPayload)
def invalid_json_payload_error(error):
    return {"message": f"'{error.payload}' is not valid JSON format"}, error.status_code

@errors.errorhandler(NoResultsFound)
def no_results_found_error(error):
    return {"message": error.message}, error.status_code

@errors.errorhandler(Exception)
def server_error(error):
    return {"message": f"Oops, got an error! {error}"}, 500
