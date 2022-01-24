from api.sources import source_config
from api.sources.generic_source import GenericSource
import requests
from datetime import datetime, timedelta
from os import getenv
import logging

class CryptoWatch(GenericSource):
    def __init__(self):
        self.url = source_config.sources["cryptowatch"]['url']
        self.hist_url = source_config.sources["cryptowatch"]['hist_url']
        self.source_name = source_config.sources["cryptowatch"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        url = self.template_url
        all_markets = requests.get(
            url=url,
            headers={"X-CW-API-Key": getenv("CRYPTOWATCH_PUBLIC_KEY")}).json()
        full_response = []
        for currency_pair in currency_pairs.split(","):
            if not self._is_valid_currency_pair(currency_pair): continue
            filtered_currencies = filter(lambda x: ":" + currency_pair.replace("_","").strip() in x[0], all_markets["result"].items())
            all_prices = {key:value for (key,value) in filtered_currencies}
            if all_prices == {}: continue
            payload = self.assemble_payload(currency_pair, all_prices)
            full_response.extend(payload)
        return full_response

    def assemble_price_payload(self, currency_pair, all_prices):
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

    def get_hist_prices(self, currency_pair, before, after, period):
        url = self.hist_url.replace("CURRENCY_PAIR", currency_pair) \
                            .replace("BEFORE_TS", before) \
                            .replace("AFTER_TS", after) \
                            .replace("PERIOD_SECONDS", period)
        hist_prices = requests.get(
            url = url,
            headers={"X-CW-API-Key": getenv("CRYPTOWATCH_PUBLIC_KEY")}).json()
        payload = self.assemble_hist_payload(hist_prices, period)
        return payload

    def assemble_hist_payload(self, hist_prices, period):
        payload = []
        if "result" not in hist_prices:
            return payload

        for candle in hist_prices["result"][str(period)]:
            open_time = datetime.fromtimestamp(candle[0]) - timedelta(hours=int(period)//60)
            payload.append({
                "open_time": int(open_time.timestamp()),
                "close_time": candle[0],
                "open_price": candle[1],
                "high_price": candle[2],
                "low_price": candle[3],
                "close_price": candle[4],
                "volume": candle[5],
                "quote_volume": candle[6],
            })
        return payload

