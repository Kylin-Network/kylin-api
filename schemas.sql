CREATE TABLE IF NOT EXISTS parachain_data (
  id SERIAL PRIMARY KEY,
  para_id VARCHAR,
  account_id VARCHAR,
  requested_block_number INT,
  processed_block_number INT,
  requested_timestamp TIMESTAMPTZ,
  processed_timestamp TIMESTAMPTZ,
  payload VARCHAR,
  feed_name VARCHAR,
  url VARCHAR,
  hash VARCHAR
);
