from dataclasses import dataclass
from datetime import datetime, timezone
import json

@dataclass(frozen=True)
class DataStore:
    para_id:str
    account_id:str
    requested_block_number:int
    processed_block_number:int
    requested_timestamp:float
    processed_timestamp:float
    payload:str
    feed_name:str
    url:str

    def to_datetime(self, timestamp):
        """
        Converts timestamp in milliseconds to datetime utc
        """
        dt = datetime.fromtimestamp(float(timestamp)/1000, tz=timezone.utc)
        return dt

    def dump_payload(self):
        return json.dumps(self.payload)
