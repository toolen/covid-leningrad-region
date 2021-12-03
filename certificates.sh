#!/usr/bin/env bash
set -euo pipefail

if [ -z "$CA_PASS" ]; then
    echo "ERROR: You must set the environment variable CA_PASS"
    exit 1
fi

CA_DIR=certificate-authority
MONGODB_DIR=mongodb/data/ssl
SCRAPER_DIR=scraper/certs
DASHBOARD_DIR=dashboard-backend/certs

# CA
echo "> Generate certificate for certificate authority"
openssl genrsa -aes256 -passout env:CA_PASS -out "$CA_DIR"/ca.key 2048
openssl req -new -x509 -days 3650 -passin env:CA_PASS -subj "/CN=ca" -key "$CA_DIR"/ca.key -sha256 -extensions v3_ca -out "$CA_DIR"/ca.crt
cat "$CA_DIR"/ca.crt "$CA_DIR"/ca.key > "$CA_DIR"/ca.pem
cp "$CA_DIR"/ca.pem "$MONGODB_DIR"/ca.pem
cp "$CA_DIR"/ca.pem "$SCRAPER_DIR"/ca.pem
cp "$CA_DIR"/ca.pem "$DASHBOARD_DIR"/ca.pem

# Server
echo "> Generating certificate for mongo"
openssl genrsa -out "$MONGODB_DIR"/mongo.key 2048
openssl req -sha256 -new -subj "/CN=mongo" -key "$MONGODB_DIR"/mongo.key -out "$MONGODB_DIR"/mongo.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$MONGODB_DIR"/mongo.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$MONGODB_DIR"/mongo.crt -days 365
openssl verify -CAfile "$CA_DIR"/ca.crt "$MONGODB_DIR"/mongo.crt
#openssl dhparam -dsaparam -out "$MONGODB_DIR"/dhparam.pem 4096
chmod 644 "$MONGODB_DIR"/mongo.*
cat "$MONGODB_DIR"/mongo.crt "$MONGODB_DIR"/mongo.key > "$MONGODB_DIR"/mongo.pem

# Client
#echo "> Generate client."
#openssl genrsa -out "$SCRAPER_DIR"/client.key 2048
#openssl req -sha256 -new -subj "/CN=mongoClient" -key "$SCRAPER_DIR"/client.key -out "$SCRAPER_DIR"/client.csr
#openssl x509 -sha256 -req -passin env:CA_PASS -in "$SCRAPER_DIR"/client.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$SCRAPER_DIR"/client.crt -days 365
#openssl verify -CAfile "$CA_DIR"/ca.crt "$SCRAPER_DIR"/client.crt
#chmod 644 "$SCRAPER_DIR"/client.*
#cat "$SCRAPER_DIR"/client.crt "$SCRAPER_DIR"/client.key > "$SCRAPER_DIR"/client.pem

# User
echo "> Generating x.509 certificate for user \"scraper\""
openssl req -sha256 -new -subj "/CN=scraper" -key "$SCRAPER_DIR"/scraper.key -out "$SCRAPER_DIR"/scraper.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$SCRAPER_DIR"/scraper.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$SCRAPER_DIR"/scraper.crt -days 365
cat "$SCRAPER_DIR"/scraper.crt "$SCRAPER_DIR"/scraper.key > "$SCRAPER_DIR"/scraper.pem

echo "> Generating x.509 certificate for user \"dashboard\""
openssl req -sha256 -new -subj "/CN=dashboard" -key "$DASHBOARD_DIR"/dashboard.key -out "$DASHBOARD_DIR"/dashboard.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$DASHBOARD_DIR"/dashboard.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$DASHBOARD_DIR"/dashboard.crt -days 365
cat "$DASHBOARD_DIR"/dashboard.crt "$DASHBOARD_DIR"/dashboard.key > "$DASHBOARD_DIR"/dashboard.pem


#https://www.grainger.xyz/creating-x-509-certificates-for-mongodb/
#openssl genrsa -out clickhouse/etc/clickhouse-server/certs/clickhouse.key 2048
#openssl req -sha256 -new -subj "/CN=clickhouse" -key clickhouse/etc/clickhouse-server/certs/clickhouse.key -out clickhouse/etc/clickhouse-server/certs/clickhouse.csr
#openssl x509 -sha256 -req -passin env:CA_PASS -in clickhouse/etc/clickhouse-server/certs/clickhouse.csr -CA certificate-authority/ca.crt -CAkey certificate-authority/ca.key -CAcreateserial -out clickhouse/etc/clickhouse-server/certs/clickhouse.crt -days 365
#openssl verify -CAfile certificate-authority/ca.crt clickhouse/etc/clickhouse-server/certs/clickhouse.crt
#openssl dhparam -dsaparam -out clickhouse/etc/clickhouse-server/certs/dhparam.pem 4096
#chmod 644 clickhouse/etc/clickhouse-server/certs/clickhouse.*
#
#openssl genrsa -out grafana/certs/grafana.key 2048
#openssl req -sha256 -new -subj "/CN=grafana" -key grafana/certs/grafana.key -out grafana/certs/grafana.csr
#openssl x509 -sha256 -req -passin env:CA_PASS -in grafana/certs/grafana.csr -CA certificate-authority/ca.crt -CAkey certificate-authority/ca.key -CAcreateserial -out grafana/certs/grafana.crt -days 365
#openssl verify -CAfile certificate-authority/ca.crt grafana/certs/grafana.crt
#chmod 644 grafana/certs/grafana.*


#https://github.com/rzhilkibaev/mongo-x509-auth-ssl/blob/master/generate-certs