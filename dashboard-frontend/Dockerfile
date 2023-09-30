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

FROM nginxinc/nginx-unprivileged:1.25.2-alpine3.18-slim@sha256:85d76ca11059254a876a26ab26d61e6ef2f0a2073e305503397dbe0864cf3c37

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

USER root

RUN apk upgrade

USER nginx

COPY ./nginx/etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html
