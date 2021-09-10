from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime
import pandas as pd
import json
class CryptoWatch(GenericSource):
    def __init__(self):
        self.url = source_config.sources["cryptowatch"]['url']
        self.source_name = source_config.sources["cryptowatch"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        url = self.template_url
        all_markets = requests.get(url).json()
        full_response = {}
        filtered_markets = pd.DataFrame(columns=['market_name', 'price'])
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            filtered_currencies = filter(lambda x: ":" + currency_pair.replace("_","").strip() in x[0], all_markets["result"].items())
            response = {key:value for (key,value) in filtered_currencies}
            current_markets = pd.DataFrame(list(response.items()), columns=['market_name', 'price'])
            current_markets['source_name'] = self.source_name
            current_markets['currency_pair'] = currency_pair
            if response == {}: continue
            filtered_markets = pd.concat([filtered_markets,current_markets])
        if len(full_response) > 0:
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response.update({"processed_at":current_timestamp,"source":self.source_name, "payload": json.loads(json.loads(json.dumps(filtered_markets.to_json(orient='records'))))})
        return full_response