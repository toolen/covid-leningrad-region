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
openssl req -new -sha256 -key "$MONGODB_DIR"/mongo.key -config "$MONGODB_DIR"/ssl.conf -out "$MONGODB_DIR"/mongo.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$MONGODB_DIR"/mongo.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$MONGODB_DIR"/mongo.crt -extensions req_ext -extfile "$MONGODB_DIR"/ssl.conf -days 365
openssl verify -CAfile "$CA_DIR"/ca.crt "$MONGODB_DIR"/mongo.crt
chmod 644 "$MONGODB_DIR"/mongo.*
cat "$MONGODB_DIR"/mongo.crt "$MONGODB_DIR"/mongo.key > "$MONGODB_DIR"/mongo.pem

# Scraper
echo "> Generating x.509 certificate for user \"scraper\""
openssl genrsa -out "$SCRAPER_DIR"/scraper.key 2048
openssl req -sha256 -new -subj "/CN=scraper" -key "$SCRAPER_DIR"/scraper.key -out "$SCRAPER_DIR"/scraper.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$SCRAPER_DIR"/scraper.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$SCRAPER_DIR"/scraper.crt -days 365
cat "$SCRAPER_DIR"/scraper.crt "$SCRAPER_DIR"/scraper.key > "$SCRAPER_DIR"/scraper.pem

# Dashboard
echo "> Generating x.509 certificate for user \"dashboard\""
openssl genrsa -out "$DASHBOARD_DIR"/dashboard.key 2048
openssl req -sha256 -new -subj "/CN=dashboard" -key "$DASHBOARD_DIR"/dashboard.key -out "$DASHBOARD_DIR"/dashboard.csr
openssl x509 -sha256 -req -passin env:CA_PASS -in "$DASHBOARD_DIR"/dashboard.csr -CA "$CA_DIR"/ca.crt -CAkey "$CA_DIR"/ca.key -CAcreateserial -out "$DASHBOARD_DIR"/dashboard.crt -days 365
cat "$DASHBOARD_DIR"/dashboard.crt "$DASHBOARD_DIR"/dashboard.key > "$DASHBOARD_DIR"/dashboard.pem
