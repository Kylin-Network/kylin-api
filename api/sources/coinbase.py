from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime

class Coinbase(GenericSource):
    def __init__(self):
        self.url = source_config.sources["coinbase"]['url']
        self.source_name = source_config.sources["coinbase"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        full_response = []
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            from_currency_symbol = currency_pair.split("_")[0].strip()
            to_currency_symbol = currency_pair.split("_")[1].strip()
            url = self.url.replace("FROM_CURRENCY",from_currency_symbol).replace("TO_CURRENCY",to_currency_symbol)
            response = requests.get(url).json()
            if "price" in response:
                price = float(response["price"])
                full_response.append(self.assemble_payload(currency_pair, price))
            else:
                continue
        return full_response
