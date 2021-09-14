from dataclasses import dataclass
import hashlib
import json

@dataclass(frozen=True)
class DataStore:
    data:object
    hash:str
    feed:str 
    block:str

    def create_data_hash(self):
        hasher = hashlib.sha256()
        encoded_data = self.dump_data().encode("utf8")
        hasher.update(encoded_data)
        return hasher.hexdigest()

    def dump_data(self):
        return json.dumps(self.data)
