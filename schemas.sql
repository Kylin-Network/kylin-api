CREATE TABLE IF NOT EXISTS parachain_data (
  id SERIAL PRIMARY KEY,
  para_id VARCHAR,
  account_id VARCHAR,
  requested_block_number BIGINT,
  processed_block_number BIGINT,
  requested_timestamp TIMESTAMP,
  processed_timestamp TIMESTAMP,
  payload VARCHAR,
  feed_name VARCHAR,
  url VARCHAR
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  wallet VARCHAR(100) UNIQUE,
  api_key VARCHAR(100)
);
