from dataclasses import dataclass
import hashlib
import json
from datetime import datetime
class DataStore():
    def __init__(self, body):
        # ToDo: Make Para_id nullable
        self.para_id = body['para_id']
        self.account_id = body['account_id']
        self.requested_block_number = int(body['requested_block_number'])
        self.processed_block_number = int(body['processed_block_number'])
        self.requested_timestamp = datetime.fromtimestamp(int(body['requested_timestamp'])/1000)
        self.processed_timestamp = datetime.fromtimestamp(int(body['processed_timestamp'])/1000)
        self.payload = body['payload']
        self.feed_name = body['feed_name']
        self.url = body['url']





    def create_data_hash(self):
        hasher = hashlib.sha256()
        encoded_data = self.dump_data().encode("utf8")
        hasher.update(encoded_data)
        return hasher.hexdigest()

    def dump_data(self):
        return json.dumps(self.data)
