FROM python:3.10-slim-buster

WORKDIR /src

COPY ./pyproject.toml /src

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /src
