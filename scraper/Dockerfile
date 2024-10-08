FROM python:3.10.13-slim-bookworm@sha256:9956522e7eafd57e3e7bb4b102d56f02882924019867cd2036c1a7c3ee56b174 AS builder

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
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN pip install --no-cache-dir poetry==$POETRY_VERSION

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry export --no-ansi --no-interaction --output requirements.txt

FROM python:3.10.13-alpine3.19@sha256:139336ea16cb3e9effd95173b94b6f0529c758cb74033f42f916289d0006917f AS runner

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
        tini==0.19.0-r2 \
    && cp /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime \
    && echo "${TIME_ZONE}" > /etc/timezone \
    && date \
    && addgroup -g 1000 -S app \
    && adduser -h /app -G app -S -u 1000 app \
    && pip install --no-cache-dir setuptools==65.5.1

COPY --chown=app:app --from=builder /code/requirements.txt /app

WORKDIR /app

USER app

RUN set -ex \
    && python -m venv --upgrade-deps venv \
    && venv/bin/pip install --no-cache-dir --require-hashes -r requirements.txt

COPY ./scraper /app/scraper

CMD ["/sbin/tini", "--", "/app/venv/bin/python", "-m", "scraper.main"]
