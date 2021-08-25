class InvalidCurrencyPair(Exception):
    def __init__(self,
                message="We didn't find any results for your query. Ensure you are using valid currency symbols with format: '<FROM-CURRENCY>_<TO-CURRENCY>'. If passing multiple currency pairs, separate them with commas. Example: btc_usd,eth_gbp,kyl_jpy",
                status_code=400):
        super().__init__(message)
        self.status_code = status_code
        