CREATE TABLE IF NOT EXISTS parachain_data (
  id SERIAL PRIMARY KEY,
  feed varchar,
  block INT,
  hash varchar,
  data varchar
);
