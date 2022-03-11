FROM node:16.14.0-bullseye-slim@sha256:11d539ac109ada08cd6644a701096d193270b3f8352aae549419d1703fd858d0 AS builder

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

FROM nginx:1.20.2-alpine@sha256:f6609f898bcdad15047629edc4033d17f9f90e2339fb5ccb97da267f16902251

LABEL maintainer="dmitrii@zakharov.cc"
LABEL org.opencontainers.image.source="https://github.com/toolen/covid-leningrad-region"

COPY --from=builder /app/dist /usr/share/nginx/html
