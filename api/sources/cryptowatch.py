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
        full_response = []
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            filtered_currencies = filter(lambda x: ":" + currency_pair.replace("_","").strip() in x[0], all_markets["result"].items())
            all_prices = {key:value for (key,value) in filtered_currencies}
            if all_prices == {}: continue
            payload = self.assemble_payload(currency_pair, all_prices)
            full_response.extend(payload)
        return full_response

    def assemble_payload(self, currency_pair, all_prices):
        payload = []
        for market, price in all_prices.items():
            payload.append({
                "currency_pair": currency_pair.lower().strip(),
                "market_name": market,
                "price": price,
                "source_name": self.source_name,
                "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        return payload
