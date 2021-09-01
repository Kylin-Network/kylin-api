class InvalidQuery(Exception):
    def __init__(self,
                message="Ensure you are using valid currency symbols with format: '<FROM-CURRENCY>_<TO-CURRENCY>'. If passing multiple currency pairs, separate them with commas. Example: btc_usd,eth_gbp,kyl_jpy",
                status_code=400,
                payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload
