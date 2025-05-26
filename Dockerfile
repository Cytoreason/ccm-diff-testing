FROM python:3.11.11-slim-bookworm

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir poetry==2.0.1 keyrings.google-artifactregistry-auth==1.1.2

ARG APP=/app
ARG SRC_DIR=src
WORKDIR $APP

ARG GOOGLE_APPLICATION_CREDENTIALS
ENV GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_REQUESTS_TIMEOUT=120

ADD pyproject.toml $APP/
ADD poetry.lock $APP/
ADD poetry.toml $APP/
ADD README.md $APP/

RUN poetry config virtualenvs.create false
RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    --mount=type=secret,id=credentials.json \
    poetry install --no-root

ADD $SRC_DIR/. $APP/$SRC_DIR/

ENV PYTHONPATH $APP:$APP/src
ENV PYTHONUNBUFFERED 1