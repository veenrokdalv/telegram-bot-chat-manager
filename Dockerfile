FROM python:3.9-slim-buster

WORKDIR /src

RUN pip install --user poetry

RUN poetry install

COPY . /src