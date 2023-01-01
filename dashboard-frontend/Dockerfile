FROM node:16.19.0-bullseye-slim@sha256:9a94201317d878b97cfc83316bc448442fe621521c0dc3ca0a4575ac9391576e AS builder

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /app

COPY package.json package-lock.json vite.config.js /app/

COPY src /app/src

WORKDIR /app

RUN set -ex \
    && npm i \
    && npm run build

FROM nginxinc/nginx-unprivileged:1.22.1-alpine@sha256:456352cd224a42ab404d62eeb2a6745013f2a5edf8ba1780fe82c46925977ae7

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

USER root

RUN apk upgrade

USER nginx

COPY ./nginx/etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html
