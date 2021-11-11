import hashlib
import json
from datetime import datetime
from api.errors.exceptions import InvalidPayload

class DataStore():
    def __init__(self, body):
        data = body['data']
        if not is_json(data["payload"]):
            raise InvalidPayload(payload=data["payload"])
            
        self.para_id = data['para_id']
        self.account_id = data['account_id']
        self.requested_block_number = int(data['requested_block_number'])
        self.processed_block_number = int(data['processed_block_number'])
        self.requested_timestamp = datetime.fromtimestamp(int(data['requested_timestamp'])/1000)
        self.processed_timestamp = datetime.fromtimestamp(int(data['processed_timestamp'])/1000)
        self.payload = data['payload'] 
        self.feed_name = data['feed_name']
        self.url = data['url']
        self.hash = body['hash']

    def create_data_hash(self):
        hasher = hashlib.sha256()
        encoded_data = self.dump_data().encode("utf8")
        hasher.update(encoded_data)
        return hasher.hexdigest()

    def dump_payload(self):
        return json.dumps(self.payload)


def is_json(json_string):
    try:
        json.loads(json_string)
    except Exception as e:
        return False
    return True
