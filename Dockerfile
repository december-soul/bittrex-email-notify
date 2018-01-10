FROM resin/raspberry-pi-alpine-python:latest

COPY . /opt/app
WORKDIR /opt/app

RUN pip install -r requirements.txt

RUN python notifications.py
