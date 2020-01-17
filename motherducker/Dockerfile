FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements.txt /tmp/

RUN apk add --no-cache --virtual .build-deps \
    gcc postgresql-dev musl-dev \
    && pip install -r /tmp/requirements.txt

WORKDIR /opt/motherducker
COPY . .