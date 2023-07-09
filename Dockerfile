FROM python:3.10

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential libssl-dev libffi-dev \
    cargo pkg-config

RUN pip install poetry==1.5.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /src
COPY . .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

CMD poetry run python shin_roulette/main.py
