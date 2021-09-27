from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class DataStore:
    para_id:str
    account_id:str
    requested_block_number:str
    processed_block_number:str
    requested_timestamp:str
    processed_timestamp:str
    payload:str
    feed_name:str
    url:str

    def generate_payload_hash(self):
        hasher = hashlib.sha256()
        encoded_data = self.dump_payload().encode("utf8")
        hasher.update(encoded_data)
        return hasher.hexdigest()

    def dump_payload(self):
        return json.dumps(self.payload)
