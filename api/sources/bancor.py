from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime

class Bancor(GenericSource):
    def __init__(self):
        self.url = source_config.sources["bancor"]['url']
        self.source_name = source_config.sources["bancor"]['source_name']
        super().__init__(self.url,self.source_name)
    def get_prices(self,currency_pairs):
        full_response = {}
        full_response[self.source_name] = {}
        rates = requests.get(self.url).json()
        ratesList = rates['data']
        print ('Hariom')
        for currency_pair in currency_pairs.split(","):
            from_currency_symbol = currency_pair.split("_")[0]                  
            response = [rate for rate in ratesList if rate['symbol'] == from_currency_symbol.upper()][0]['price']
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair] = {"processed_at":current_timestamp,"source":currency_pairs, "payload":response}
        return full_response    
