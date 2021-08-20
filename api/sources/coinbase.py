from api.sources import source_config
from api.sources.generic_source import GenericSource

class Coinbase(GenericSource):
    def __init__(self):
        self.url = source_config.sources["coinbase"]['url']
        self.source_name = source_config.sources["coinbase"]['source_name']
        super().__init__(self.url,self.source_name)

    def get_prices(self,currency_pairs):
        return super().get_price(currency_pairs)
