FROM python:3.10.0-slim-bullseye@sha256:95bebb8af5996a5c2ad12526170fc599ff281bb823434b9f946335c35ebc5f2b AS development_build

LABEL maintainer="dmitrii@zakharov.cc"

ARG APP_ENV

ENV APP_ENV=${APP_ENV} \
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
  POETRY_VERSION=1.1.12 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.local/bin"


# System deps:
RUN set -exo \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    # Defining build-time-only dependencies:
    curl=7.74.0-1.3+b1 \
  # Installing `tini` utility:
  # https://github.com/krallin/tini
  && curl -sOL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
  && curl -sOL "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini.sha256sum" \
  && sha256sum -c tini.sha256sum \
  && mv tini /usr/local/bin/tini \
  && chmod +x /usr/local/bin/tini \
  && tini --version \
  && rm -rf tini.sha256sum \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Removing build-time-only dependencies:
  && apt-get remove -y curl \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Setting up proper permissions:
RUN set -exo \
  && groupadd -g 1000 -r app \
  && useradd -u 1000 -d /code -r -g app app \
  && chown app:app -R /code

# Copy only requirements, to cache them in docker layer
COPY --chown=app:app ./poetry.lock ./pyproject.toml /code/

# Project initialization:
RUN poetry install --no-interaction --no-ansi \
  # Cleaning poetry installation's cache for production:
  && if [ "$APP_ENV" = "production" ]; then rm -rf "$POETRY_CACHE_DIR"; fi

# Running as non-root user:
USER app

# We customize how our app is loaded with the custom entrypoint:
CMD ["tini", "--", "python", "-m", "scraper.main"]


# The following stage is only for Prod:
# https://wemake-django-template.readthedocs.io/en/latest/pages/template/production.html
FROM development_build AS production_build
COPY --chown=app:app . /code
