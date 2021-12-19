"""This file contains configuration properties."""
import os

from scraper.utils import avoid_empty_value, email_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS_DIR = os.path.join(BASE_DIR, "certs")

default_tls_cert_key_path = f"{CERTS_DIR}/scraper.pem"
if not os.path.exists(default_tls_cert_key_path):
    default_tls_cert_key_path = ""

default_ca_path = f"{CERTS_DIR}/ca.pem"
if not os.path.exists(default_ca_path):
    default_ca_path = ""

URL = os.getenv("SCRAPER_URL", "http://localhost:8888/06-11-21.html")
DB_URI = os.getenv(
    "SCRAPER_DB_URI",
    "mongodb://localhost:27017/covid_stat?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
)
DB_NAME = os.getenv("SCRAPER_DB_NAME", "covid_stat")
DB_COLLECTION_NAME = os.getenv("SCRAPER_DB_COLLECTION_NAME", "leningrad_region")
TLS_CERT_KEY_PATH = os.getenv("SCRAPER_TLS_CERT_KEY_PATH", default_tls_cert_key_path)
TLS_CA_PATH = os.getenv("SCRAPER_TLS_CA_PATH", default_ca_path)
EMAIL_URL = email_url(os.getenv("SCRAPER_EMAIL_URL", "smtp://localhost:1025"))
DEFAULT_FROM_EMAIL = avoid_empty_value(os.getenv("SCRAPER_DEFAULT_FROM_EMAIL"))
ADMIN_EMAIL = avoid_empty_value(os.getenv("SCRAPER_ADMIN_EMAIL"))
