# Kylin API

This API is set up for use with Python >= 3.7 and [Docker](https://www.docker.com/). You can set-up your local environment manually or compose up with docker to launch a containerised version of the API.
```bash
git clone https://github.com/Kylin-Network/kylin-api.git
```

## Running with Docker

To run the server with Docker, you'll need to [install Docker](https://www.docker.com/products/docker-desktop) if you havent already. Then, you can run:
```bash
docker-compose up -d
```

This will start three Docker containers:
- kylin-api: [Gunicorn](https://gunicorn.org/) server that wraps the Flask app defined in `api/app.py`
- postgres: [PostgreSQL](https://www.postgresql.org/) database
- redis: [Redis](https://redis.io/topics/introduction) database and memory cache

You should now be able to send:

```bash
curl localhost:8080/health
```

And receive the response `OK` and status code `200`. You can see other example calls, [here](#example-calls). 

Your server and database are running in a detached state as indicated by `-d`. When you are ready to bring down your server, run:

```bash
docker-compose down
```

## Running Locally

To run the server locally, you'll need to install a few requirements. To do this, run:

```bash
pip install -r requirements/common.txt
``` 

If you are running a local PostgreSQL instance, create an 'SQLALCHEMY_DATABASE_URI' environment variable:
```bash
export SQLALCHEMY_DATABASE_URI=YOUR_CONNECTION_STRING
```
If you plan on writing to the database, you'll need to create a `parachain_data` and `user` table as defined in `schemas.sql`.

To enable rate limits, declare your 'RATELIMIT_STORAGE_URL' environment variable:
```bash
export RATELIMIT_STORAGE_URL=YOUR_CONNECTION_STRING
```

Finally, to boot up the server, run:

```bash
bash bin/run.sh
``` 

You should now be able to interact with your server as described above.

## Example Calls
Get API key:
```bash
curl -d '{"wallet": "YOUR WALLET ADDRESS"}' -H "Content-Type: application/json" "http://localhost:8080/auth/register"
```
Get price feed:
```bash
curl -H "x-api-key: YOUR_API_KEY" "http://localhost:8080/prices/spot?currency_pairs=btc_usd"
```
Write to database:
```bash
curl -d '{"para_id": "para id", "account_id": "account id", "requested_block_number": "1", "processed_block_number": "1", "requested_timestamp": "1632770041.806915", "processed_timestamp": "1632770041.806915", "payload": "This is json serializable data", "feed_name": "demo_feed", "url": "url"}' -H "x-api-key: YOUR_API_KEY" -H "Content-Type: application/json" "http://localhost:8080/parachain/submit"
```
Query database:
```bash
# select all data
curl -H "x-api-key: YOUR_API_KEY" "http://localhost:8080/parachain/query/all"

# select by feed
curl -H "x-api-key: YOUR_API_KEY" "http://localhost:8080/parachain/query?feed=demo_feed"

# query with sql
curl -H "x-api-key: YOUR_API_KEY" "http://localhost:8080/parachain/query/sql?query=SELECT%20*%20FROM%20parachain_data"
```

## Testing the API

Testing the API is set up using `pytest`. To execute tests you can install the project's development dependencies with:

```bash
pip install -r requirements/develop.txt
```
Then from the root directory, run:
```bash
pytest
```
This runs `tests/test_api.py` which contains test functions.

## Accessing the Swagger 
With the application running, use the browser to search the following:
```bash
http://localhost:8080/
```

You can see the API's specification and try it directly from the swagger UI.  

Inside each namespace you will see the list of the endpoints available. You can test them using the `try_out` button.
