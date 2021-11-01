#!/usr/bin/env bash

aws s3 cp s3://kylin-api-bucket/secret.txt .env
set -a
source .env
set +a

gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4