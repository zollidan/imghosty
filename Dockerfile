FROM python:3.10-slim

WORKDIR /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .

COPY .env .

RUN pip install -r requirements.txt

COPY . . 