from api.sources.cryptocompare import CryptoCompare
from api.sources.cryptowatch import CryptoWatch
from api.sources.bancor import Bancor
from api.sources.coingecko import CoinGecko
from api.sources.coinbase import Coinbase
from datetime import datetime
import logging
import traceback

class OracleFramework:
    def get_prices(self,currency_pairs):
        sources = {CoinGecko,CryptoCompare,CryptoWatch,Bancor,Coinbase,}
        full_response = {}
        full_response['sources'] = {}
        full_response['started_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for source in sources:
            try:
                prices = source().get_prices(currency_pairs)
                full_response['sources'].update(prices)
            except Exception as e:
                logging.error(traceback.format_exc())
        full_response['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return full_response

    def has_results(self, full_response):
        """
        Helper function used to determine if dictionary returned from OracleFramework.get_prices() contains price data or not
        """
        for source_response in full_response["sources"].values():
            if source_response: return True
        return False
