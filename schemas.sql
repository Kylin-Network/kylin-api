CREATE TABLE IF NOT EXISTS parachain_data (
  id SERIAL PRIMARY KEY,
  para_id varchar,
  account_id varchar,
  requested_block_number bigint,
  processed_block_number bigint,
  requested_timestamp timestamp,
  processed_timestamp timestamp,
  payload varchar,
  feed_name varchar,
  url varchar,
  hash varchar
);
