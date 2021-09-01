from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime

class CoinGecko(GenericSource):
    def __init__(self):
        self.url = source_config.sources["coingecko"]['url']
        self.source_name = source_config.sources["coingecko"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        full_response = {}
        full_response[self.source_name] = {}
        symbol_lookup_url = self.url.replace("simple/price?ids=FROM_CURRENCY&vs_currencies=TO_CURRENCY","coins/list/")
        all_coins = requests.get(symbol_lookup_url).json()
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            from_currency_symbol = currency_pair.split("_")[0].strip()
            to_currency_symbol = currency_pair.split("_")[1].strip()
            filtered_currency = filter(lambda x: x["symbol"]==from_currency_symbol.lower(), all_coins)
            filtered_currency = self._has_next(filtered_currency)
            if filtered_currency is None: continue
            response = requests.get(self.url.replace("FROM_CURRENCY",filtered_currency["id"]).replace("TO_CURRENCY",to_currency_symbol)).json()
            if (filtered_currency["id"] in response) and (to_currency_symbol.lower() in response[filtered_currency["id"]]):
                price = float(response[filtered_currency["id"]][to_currency_symbol.lower()])
            else:
                continue
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair.strip().lower()] = {"processed_at":current_timestamp,"source":self.source_name, "payload":price}
        return full_response
