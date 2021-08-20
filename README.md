# kylin-api

This API is set up for use with Python >= 3.7 and [Docker](https://www.docker.com/). You can set-up your local environment manually or compose up with docker to launch a containerised version of the API.

## Running locally

To run the server, you'll need to install a few requirements. To do this, run:

```bash
pip install -r requirements/common.txt
```

This will install only the dependencies required to run the server. To boot up the server, you can run:

```bash
bash bin/run.sh
```

This will start a [Gunicorn](https://gunicorn.org/) server that wraps the Flask app defined in `api/app.py`. 

You should now be able to send:

```bash
curl localhost:8080/health
```

And receive the response `OK` and status code `200`. 

## Running with docker

Unsurprisingly, you'll need [Docker](https://www.docker.com/products/docker-desktop) 
installed to run this project with Docker. To launch a containerised version of the API, run:
```bash
docker compose up -d
```

Your server will boot up in a detached state as indicated by `-d`, and should be accessible as before. When you are ready to bring down your server, run:

```bash
docker compose down
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
Make sure the application is running in your local. 

The swagger endpoint is mapped to the `/swagger`

You can see the API specifictaion and the try your application directly from the swagger ui in the browser.

Go to the browser and paste the following

```bash
http://localhost:8080/swagger
```

You will be able to see the default namespace,click there and you can see the list of the endpoints available
play through it using the try_out button



