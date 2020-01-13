FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY ./motherducker/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/motherducker
COPY ./motherducker/ /opt/motherducker/
