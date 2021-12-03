"""This file contains configuration properties."""
import os

URL = os.getenv("SCRAPER_URL", "http://localhost:8888/06-11-21.html")
DB_URI = os.getenv("SCRAPER_DB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("SCRAPER_DB_NAME", "covid_stat")
DB_COLLECTION_NAME = os.getenv("SCRAPER_DB_COLLECTION_NAME", "leningrad_region")
TLS_CERT_KEY_PATH = os.getenv("SCRAPER_TLS_CERT_KEY_PATH")
TLS_CA_PATH = os.getenv("SCRAPER_TLS_CA_PATH")
