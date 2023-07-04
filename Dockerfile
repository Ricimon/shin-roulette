FROM python:3.10

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /src
COPY . .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN poetry install --no-dev && rm -rf $POETRY_CACHE_DIR

CMD poetry run python shin_roulette/main.py
