FROM python:3.10.7-slim-bullseye@sha256:7e8d32d9e8c20a3626146a932ecf98c3fc2a4b1100b008193b835acc2ab88018 AS builder

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

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
    POETRY_VERSION=1.1.14 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry export --no-ansi --no-interaction --output requirements.txt

FROM python:3.10.7-alpine3.16@sha256:f34ed96bfd9f329f89ce3977373cef37ce5d0a4ba8c5ed4aebca785d649b9082 AS runner

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

ENV \
    TIME_ZONE=Europe/Moscow \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN set -ex \
    && apk upgrade \
    && apk add --no-cache \
        tini==0.19.0-r0 \
    && cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && date \
    && addgroup -g 1000 -S app \
    && adduser -h /app -G app -S -u 1000 app

COPY --chown=app:app --from=builder /code/requirements.txt /app

WORKDIR /app

USER app

RUN set -ex \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --require-hashes -r requirements.txt

COPY ./scraper /app/scraper

CMD ["/sbin/tini", "--", "/app/venv/bin/python", "-m", "scraper.main"]
