from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests

class Bancor(GenericSource):
    def __init__(self):
        self.url = source_config.sources["bancor"]['url']
        self.source_name = source_config.sources["bancor"]['source_name']
        super().__init__(self.url,self.source_name)
        
    def get_prices(self,currency_pairs):
        full_response = []
        all_markets = requests.get(self.url).json()
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            from_currency_symbol = currency_pair.split("_")[0].strip()
            to_currency_symbol = currency_pair.split("_")[1].strip()
            if "usd" not in to_currency_symbol.lower(): continue # bancor only supports usd
            filtered_currency = filter(lambda x: from_currency_symbol.upper()==x["symbol"], all_markets["data"])
            response = self._has_next(filtered_currency)
            if response is None:
                continue
            else:
                price = float(response["price"]["usd"])
                full_response.append(self.assemble_payload(currency_pair, price))
        return full_response    
