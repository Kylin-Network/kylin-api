import requests
from datetime import datetime

class GenericSource:
    def __init__(self,url,source_name):
        self.template_url = url
        self.source_name = source_name

    def get_source_name(self):
        return self.source_name

    def has_next(self, generator:object):
        try:
            first = next(generator)
        except StopIteration:
            return None
        return first
    
    def is_valid_currency_pair(self, currency_pair):
        split_currencies = currency_pair.split("_")
        if len(split_currencies) != 2: return False
        rules = [
            split_currencies[0].isalpha(),
            split_currencies[1].isalpha(),
        ]
        return True if all(rules) else False

    def get_price(self,currency_pairs):
        full_response = {}
        full_response[self.source_name] = {}
        for currency_pair in currency_pairs.split(","):
            from_currency = currency_pair.split("_")[0]
            to_currency = currency_pair.split("_")[1]
            url = self.template_url.replace("FROM_CURRENCY",from_currency).replace("TO_CURRENCY",to_currency)
            response = requests.get(url).json()
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair] = {"processed_at":current_timestamp,"source":self.source_name, "payload":response}
        return full_response
        
