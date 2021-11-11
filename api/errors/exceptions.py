class InvalidCurrencyPair(Exception):
    def __init__(self,
            message="Invalid currency pair",
            status_code=404,
            payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class InvalidContentType(Exception):
    def __init__(self,
            message="Invalid content-type",
            status_code=400,
            payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class InvalidSubmitParam(Exception):
    def __init__(self,
            message="Invalid submit param(s)",
            status_code=400,
            payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class InvalidQueryParam(Exception):
    def __init__(self,
            message="Invalid query param(s)",
            status_code=400,
            payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload

class InvalidPayload(Exception):
    def __init__(self,
            message="Payload is not valid JSON",
            status_code=422,
            payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        