FROM python:3.7
ENV PYTHONUNBUFFERED 1

COPY ./motherducker/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /opt/motherducker
COPY ./motherducker/ /opt/motherducker/

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME