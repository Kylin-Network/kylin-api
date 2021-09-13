CREATE TABLE IF NOT EXISTS parachain_data (
  id SERIAL PRIMARY KEY,
  feed varchar,
  block BIGINT,
  hash varchar,
  data varchar
);
