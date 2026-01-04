FROM node:18.19.0-bullseye-slim@sha256:b816d45defe8dc6a07321f05b7e58a841f97e612f6f6ea0a3be44ea7d77474a1 AS builder

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

FROM nginxinc/nginx-unprivileged:1.29.3-alpine3.22@sha256:42c794e539b375187fa8b34b8b3f693a919b0ce8009a85e862caf39186c10b4f

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

ENV \
    BUSYBOX_VERSION=1.37.0-r20

USER root

RUN \
   apk update && \
   apk add --no-cache busybox=$BUSYBOX_VERSION

USER nginx

#COPY ./nginx/etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080
