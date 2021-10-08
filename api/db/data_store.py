from dataclasses import dataclass
from datetime import datetime, timezone

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

    def to_datetime(self, timestamp):
        """
        Converts a timestamp in milliseconds to datetime utc
        """
        dt = datetime.fromtimestamp(self.from_millis(timestamp), tz=timezone.utc)
        return dt

    def from_millis(self, val):
        return float(val) / 1000
