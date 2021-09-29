from flask_sqlalchemy import SQLAlchemy
from api.db.data_store import DataStore
import json

db = SQLAlchemy()

class ParachainDB(db.Model):
    __tablename__ = 'parachain_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    para_id = db.Column(db.String)
    account_id = db.Column(db.String)
    requested_block_number = db.Column(db.BigInteger)
    processed_block_number = db.Column(db.BigInteger)
    requested_timestamp = db.Column(db.DateTime)
    processed_timestamp = db.Column(db.DateTime)
    payload = db.Column(db.String)
    feed_name = db.Column(db.String)
    url = db.Column(db.String)

    @classmethod
    def select_all(self):
        # query_with_sql = db.engine.execute("SELECT * FROM parachain_data")
        data = ParachainDB.query.all()
        return convert_model_obj_to_list(data)
    
    @classmethod
    def select_all_by_hash(self, hash):
        feed = db.session.query(ParachainDB) \
            .filter_by(hash=hash) \
            .first() \
            .feed
        return select_all_by_feed(feed)

    @classmethod
    def select_all_by_feed(self, feed):
        data = db.session.query(ParachainDB) \
            .filter_by(feed=feed) \
            .order_by(ParachainDB.block) \
            .all()
        return convert_model_obj_to_list(data)

    @classmethod
    def convert_model_obj_to_list(self, model):
        payload = [{
            "feed":row.feed,
            "block": row.block,
            "hash": row.hash,
            "data": json.loads(row.data)
            } for row in model
        ]
        return payload

    @classmethod
    def insert_new_row(self, data_request:DataStore):
        insert = ParachainDB(
            para_id=data_request.para_id,
            account_id=data_request.account_id,
            requested_block_number=data_request.requested_block_number,
            processed_block_number=data_request.processed_block_number,
            requested_timestamp=data_request.requested_timestamp,
            processed_timestamp=data_request.processed_timestamp,
            payload=data_request.payload,
            feed_name=data_request.feed_name,
            url = data_request.url
        )
        db.session.add(insert)
        db.session.commit()
