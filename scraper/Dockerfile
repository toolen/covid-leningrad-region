FROM python:3.9.7-slim-buster AS development_build

LABEL maintainer="dmitrii@zakharov.cc"

ARG APP_ENV

ENV APP_ENV=${APP_ENV} \
  # build:
  BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # tini:
  TINI_VERSION=v0.19.0 \
  # poetry:
  POETRY_VERSION=1.1.7 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"


# System deps:
RUN \
  set -eox \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    # Defining build-time-only dependencies:
    $BUILD_ONLY_PACKAGES \
  # Installing `tini` utility:
  # https://github.com/krallin/tini
  && wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
  && chmod +x /usr/local/bin/tini \
  && tini --version \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && wget -O- 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  # Removing build-time-only dependencies:
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Setting up proper permissions:
RUN \
  set -eox \
  && groupadd -g 1000 -r app \
  && useradd -u 1000 -d /code -r -g app app \
  && chown app:app -R /code

# Copy only requirements, to cache them in docker layer
COPY --chown=app:app ./poetry.lock ./pyproject.toml /code/

# Project initialization:
RUN echo "$APP_ENV" && poetry version \
  && poetry install \
    $(if [ "$APP_ENV" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction --no-ansi \
  # Upgrading pip, it is insecure, remove after `pip@21.1`
  && poetry run pip install -U pip \
  # Cleaning poetry installation's cache for production:
  && if [ "$APP_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

# Running as non-root user:
USER app

# We customize how our app is loaded with the custom entrypoint:
CMD ["tini", "--", "python", "-m", "scraper.main"]


# The following stage is only for Prod:
# https://wemake-django-template.readthedocs.io/en/latest/pages/template/production.html
FROM development_build AS production_build
COPY --chown=app:app . /code
