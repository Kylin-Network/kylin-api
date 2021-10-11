from dataclasses import dataclass
from datetime import datetime, timezone
import json

# @dataclass(frozen=True)
class DataRequest:
    def __init__(self, body):
        self.para_id = body["para_id"]
        self.account_id = body["account_id"]
        self.requested_block_number = int(body["requested_block_number"])
        self.processed_block_number = int(body["processed_block_number"])
        self.requested_timestamp = datetime.fromtimestamp(int(body["requested_timestamp"])/1000)
        self.processed_timestamp = datetime.fromtimestamp(int(body["processed_timestamp"])/1000)
        self.payload = body["payload"]
        self.feed_name = body["feed_name"]
        self.url = body["url"]
