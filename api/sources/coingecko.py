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
            from_currency_symbol = currency_pair.split("_")[0]
            to_currency_symbol = currency_pair.split("_")[1]
            from_currency_id = [coin for coin in all_coins if coin['symbol'] == from_currency_symbol.lower()][0]['id']
            response = requests.get(self.url.replace("FROM_CURRENCY",from_currency_id).replace("TO_CURRENCY",to_currency_symbol)).json()
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair] = {"processed_at":current_timestamp,"source":self.source_name, "payload":response}
        return full_response
