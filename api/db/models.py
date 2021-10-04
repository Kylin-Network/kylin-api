from flask_sqlalchemy import SQLAlchemy
from api.db.data_store import DataStore
from datetime import datetime, timezone

db = SQLAlchemy()

class ParachainData(db.Model):
    __tablename__ = 'parachain_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    para_id = db.Column(db.String)
    account_id = db.Column(db.String)
    requested_block_number = db.Column(db.Integer)
    processed_block_number = db.Column(db.Integer)
    requested_timestamp = db.Column(db.DateTime)
    processed_timestamp = db.Column(db.DateTime)
    payload = db.Column(db.String)
    feed_name = db.Column(db.String)
    url = db.Column(db.String)
    hash = db.Column(db.String)

    @classmethod
    def sql(self, query):
        data = db.engine.execute(query)
        return self.convert_sql_query_to_list(data)

    @classmethod
    def select_all(self):
        data = ParachainData.query.all()
        return self.convert_model_obj_to_list(data)
    
    @classmethod
    def select_all_by_hash(self, hash):
        feed = db.session.query(ParachainData) \
            .filter_by(hash=hash) \
            .first() \
            .feed
        return self.select_all_by_feed(feed)

    @classmethod
    def select_all_by_feed(self, feed):
        data = db.session.query(ParachainData) \
            .filter_by(feed_name=feed) \
            .order_by(ParachainData.processed_timestamp) \
            .all()
        return self.convert_model_obj_to_list(data)

    @classmethod
    def convert_model_obj_to_list(self, model):
        payload = [{
            "para_id": row.para_id,
            "account_id": row.account_id,
            "requested_block_number": row.requested_block_number,
            "processed_block_number": row.processed_block_number,
            "requested_timestamp": row.requested_timestamp,
            "processed_timestamp": row.processed_timestamp,
            "payload": row.payload,
            "feed_name": row.feed_name,
            "url": row.url,
            "hash": row.hash,
            } for row in model
        ]
        return payload

    @classmethod
    def convert_sql_query_to_list(self, list_of_rows):
        payload = [{
            "id": row[0],
            "para_id": row[1],
            "account_id": row[2],
            "requested_block_number": row[3],
            "processed_block_number": row[4],
            "requested_timestamp": row[5],
            "processed_timestamp": row[6],
            "payload": row[7],
            "feed_name": row[8],
            "url": row[9],
            "hash": row[10],
            } for row in list_of_rows
        ]
        return payload

    @classmethod
    def insert_new_row(self, store:DataStore):
        insert = ParachainData(
            para_id = store.para_id,
            account_id = store.account_id,
            requested_block_number = int(store.requested_block_number),
            processed_block_number = int(store.processed_block_number),
            requested_timestamp = datetime.fromtimestamp(float(store.requested_timestamp), tz=timezone.utc),
            processed_timestamp = datetime.fromtimestamp(float(store.processed_timestamp), tz=timezone.utc),
            payload = store.payload,
            feed_name = store.feed_name,
            url = store.url,
            hash = store.generate_payload_hash(),
        )
        db.session.add(insert)
        db.session.commit()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(100), unique=True)
    api_key = db.Column(db.String(100))
