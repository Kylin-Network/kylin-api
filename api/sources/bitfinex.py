from api.sources import source_config
from api.sources.generic_source import GenericSource

class Bitfinex(GenericSource):
    def __init__(self):
        self.url = source_config.sources["bitfinex"]['url']
        self.source_name = source_config.sources["bitfinex"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        return super().get_price(currency_pairs)
