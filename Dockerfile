FROM python:3.13.0a4-slim

COPY requirements/common.txt requirements/common.txt
RUN pip install -U pip && pip install -r requirements/common.txt

COPY ./api /app/api
COPY ./bin /app/bin
COPY wsgi.py /app/wsgi.py
WORKDIR /app

RUN useradd kylin
USER kylin

EXPOSE 8080

ENTRYPOINT ["bash", "/app/bin/run.sh"]