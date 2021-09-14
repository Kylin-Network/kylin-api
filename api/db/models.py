from flask_sqlalchemy import SQLAlchemy
from api.db.data_store import DataStore
import json

db = SQLAlchemy()

class ParachainDB(db.Model):
    __tablename__ = 'parachain_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feed = db.Column(db.String)
    block = db.Column(db.Integer)
    hash = db.Column(db.String)
    data = db.Column(db.String)

    @classmethod
    def select_all(self):
        # query_with_sql = db.engine.execute("SELECT * FROM parachain_data")
        data = ParachainDB.query.all()
        return self.convert_model_obj_to_list(data)
    
    @classmethod
    def select_all_by_hash(self, hash):
        feed = db.session.query(ParachainDB) \
            .filter_by(hash=hash) \
            .first() \
            .feed
        return self.select_all_by_feed(feed)

    @classmethod
    def select_all_by_feed(self, feed):
        data = db.session.query(ParachainDB) \
            .filter_by(feed=feed) \
            .order_by(ParachainDB.block) \
            .all()
        return self.convert_model_obj_to_list(data)

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
    def insert_new_row(self, store:DataStore):
        insert = ParachainDB(
            feed=store.feed,
            block=int(store.block),
            hash=store.hash,
            data=store.dump_data(),
        )
        db.session.add(insert)
        db.session.commit()
