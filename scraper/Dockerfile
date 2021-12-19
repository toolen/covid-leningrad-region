FROM python:3.10.1-slim-bullseye@sha256:9f702aa0f2bd7fe7a43bcf46e487040ba3237f2115994ae74ea7b270479ea8f3 AS builder

LABEL maintainer="dmitrii@zakharov.cc"

ENV \
    DEBIAN_FRONTEND=noninteractive \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry install --no-dev --no-ansi --no-interaction

COPY ./scraper /code/scraper

RUN poetry build --no-ansi --no-interaction


FROM python:3.10.1-alpine3.15@sha256:affe0faa14e7553fc570beec3864e74b5e36f8c19b2bb49ae8ba79c0e9e7236e AS runner

ENV \
    TIME_ZONE=Europe/Moscow \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # tini:
    TINI_VERSION=v0.19.0

RUN apk add --no-cache \
#        curl==7.80.0-r0 \
        tini==0.19.0-r0 \
    && cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && date \
    && addgroup -g 1000 -S app \
    && adduser -h /app -G app -S -u 1000 app

COPY --chown=app:app --from=builder /code/dist/scraper-*.whl /app

WORKDIR /app

USER app

RUN set -ex \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --target /app/scraper -- scraper-*.whl

WORKDIR /app/scraper

CMD ["/sbin/tini", "--", "/app/venv/bin/python", "-m", "scraper.main"]













#ARG APP_ENV
#
#ENV APP_ENV=${APP_ENV} \
#  # python:
#  PYTHONFAULTHANDLER=1 \
#  PYTHONHASHSEED=random \
#  PYTHONDONTWRITEBYTECODE=1 \
#  # pip:
#  PIP_NO_CACHE_DIR=off \
#  PIP_DISABLE_PIP_VERSION_CHECK=on \
#  PIP_DEFAULT_TIMEOUT=100 \
#  # tini:
#  TINI_VERSION=v0.19.0 \
#  # poetry:
#  POETRY_VERSION=1.1.12 \
#  POETRY_NO_INTERACTION=1 \
#  POETRY_VIRTUALENVS_CREATE=false \
#  POETRY_CACHE_DIR='/var/cache/pypoetry' \
#  PATH="$PATH:/root/.local/bin"
#
#
## System deps:
#SHELL ["/bin/bash", "-o", "pipefail", "-c"]
#RUN set -exo \
#  && apt-get update \
#  && apt-get upgrade -y \
#  && apt-get install --no-install-recommends -y \
#    # Defining build-time-only dependencies:
#    curl=7.74.0-1.3+b1 \
#  # Installing `tini` utility:
#  # https://github.com/krallin/tini
#  && curl -sOL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
#  && curl -sOL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.sha256sum" \
#  && sha256sum -c tini.sha256sum \
#  && mv tini /usr/local/bin/tini \
#  && chmod +x /usr/local/bin/tini \
#  && tini --version \
#  && rm -rf tini.sha256sum \
#  # Installing `poetry` package manager:
#  # https://github.com/python-poetry/poetry
#  && curl -sSL 'https://install.python-poetry.org' | python - \
#  && poetry --version \
#  # Removing build-time-only dependencies:
#  && apt-get remove -y curl \
#  # Cleaning cache:
#  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
#  && apt-get clean -y \
#  && rm -rf /var/lib/apt/lists/*
#
#WORKDIR /code
#
## Setting up proper permissions:
#RUN set -exo \
#  && groupadd -g 1000 -r app \
#  && useradd -u 1000 -d /code -r -g app app \
#  && chown app:app -R /code
#
## Copy only requirements, to cache them in docker layer
#COPY --chown=app:app ./poetry.lock ./pyproject.toml /code/
#
## Project initialization:
#RUN poetry install --no-dev --no-interaction --no-ansi \
#  # Cleaning poetry installation's cache for production:
#  && rm -rf "$POETRY_CACHE_DIR"
#
## Copy source code
#COPY --chown=app:app ./scraper /code/scraper
#
## Running as non-root user:
#USER app
#
## We customize how our app is loaded with the custom entrypoint:
#CMD ["/sbin/tini", "--", "python", "-m", "scraper.main"]
