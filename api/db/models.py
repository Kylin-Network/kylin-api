from flask_sqlalchemy import SQLAlchemy
from api.db.data_store import DataStore

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

    @classmethod
    def select_all_by_feed(self, feed):
        result = db.session.query(ParachainData) \
            .filter_by(feed_name=feed) \
            .order_by(ParachainData.processed_timestamp) \
            .all()
        return [ParachainData.row_to_dict(row) for row in result]

    @classmethod
    def row_to_dict(self, row):
        payload = {}
        for column in row.__table__.columns:
            payload[column.name] = str(getattr(row, column.name))
        return payload

    @classmethod
    def insert_new_row(self, store:DataStore):
        insert = ParachainData(
            para_id = store.para_id,
            account_id = store.account_id,
            requested_block_number = int(store.requested_block_number),
            processed_block_number = int(store.processed_block_number),
            requested_timestamp = store.to_datetime(store.requested_timestamp),
            processed_timestamp = store.to_datetime(store.processed_timestamp),
            payload = store.payload,
            feed_name = store.feed_name,
            url = store.url,
        )
        db.session.add(insert)
        db.session.commit()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(100), unique=True)
    api_key = db.Column(db.String(100))
