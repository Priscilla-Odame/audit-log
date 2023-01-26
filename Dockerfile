FROM python:3.9.12-slim

WORKDIR /app

ADD . /app

RUN apt-get update

RUN pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

EXPOSE 5000