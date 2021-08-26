import requests
from datetime import datetime

class GenericSource:
    def __init__(self,url,source_name):
        self.template_url = url
        self.source_name = source_name

    def get_source_name(self):
        return self.source_name
    
    def get_prices(self,currency_pairs):
        full_response = {}
        full_response[self.source_name] = {}
        for currency_pair in currency_pairs.split(","):
            from_currency = currency_pair.split("_")[0].strip()
            to_currency = currency_pair.split("_")[1].strip()
            url = self.template_url.replace("FROM_CURRENCY",from_currency).replace("TO_CURRENCY",to_currency)
            response = requests.get(url).json()
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair.strip().lower()] = {"processed_at":current_timestamp,"source":self.source_name, "payload":response}
        return full_response

    def _has_next(self, generator:object):
        """
        Helper function used to determine if a generator object contains a value or is empty
        """
        try:
            first = next(generator)
        except StopIteration:
            return None
        return first
    
    def _is_valid_currency_pair(self, currency_pair):
        """
        Helper function used to check if currency_pair is valid format
        """
        split_currencies = currency_pair.split("_")
        if len(split_currencies) != 2: return False
        rules = [
            split_currencies[0].strip().isalpha(),
            split_currencies[1].strip().isalpha(),
        ]
        return True if all(rules) else False
        
