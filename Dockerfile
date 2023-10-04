FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG POETRY_VERSION=1.6.1

WORKDIR /code/

RUN pip install --upgrade pip && pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY ["pyproject.toml", "poetry.lock", "./"]

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-ansi --no-interaction

COPY ./src/ /code/
