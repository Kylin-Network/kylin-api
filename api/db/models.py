from flask_sqlalchemy import SQLAlchemy
from api.db.data_store import DataStore

db = SQLAlchemy()

class ParachainData(db.Model):
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
    def insert_new_row(self, data_request:DataStore):
        insert = ParachainData(
            para_id = data_request.para_id,
            account_id = data_request.account_id,
            requested_block_number = int(data_request.requested_block_number),
            processed_block_number = int(data_request.processed_block_number),
            requested_timestamp = data_request.to_datetime(data_request.requested_timestamp),
            processed_timestamp = data_request.to_datetime(data_request.processed_timestamp),
            payload = data_request.payload,
            feed_name = data_request.feed_name,
            url = data_request.url,
        )
        db.session.add(insert)
        db.session.commit()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    wallet = db.Column(db.String(100), unique=True)
    api_key = db.Column(db.String(100))
