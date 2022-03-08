"""This file contains configuration properties."""
import os
from typing import Dict, Union

from scraper.utils import avoid_empty_value, email_url

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS_DIR: str = os.path.join(BASE_DIR, "certs")

default_tls_cert_key_path: str = f"{CERTS_DIR}/scraper.pem"
if not os.path.exists(default_tls_cert_key_path):
    default_tls_cert_key_path = ""

default_ca_path: str = f"{CERTS_DIR}/ca.pem"
if not os.path.exists(default_ca_path):
    default_ca_path = ""

URL: str = os.getenv("SCRAPER_URL", "http://localhost:8888/page.html")
DB_URI: str = os.getenv(
    "SCRAPER_DB_URI",
    "mongodb://localhost:27017/covid_stat?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority",
)
DB_NAME: str = os.getenv("SCRAPER_DB_NAME", "covid_stat")
DB_COLLECTION_NAME: str = os.getenv("SCRAPER_DB_COLLECTION_NAME", "leningrad_region")
TLS_CERT_KEY_PATH: str = os.getenv(
    "SCRAPER_TLS_CERT_KEY_PATH", default_tls_cert_key_path
)
TLS_CA_PATH: str = os.getenv("SCRAPER_TLS_CA_PATH", default_ca_path)
EMAIL_URL: Dict[str, Union[str, int, bool]] = email_url(
    os.getenv("SCRAPER_EMAIL_URL", "smtp://localhost:1025")
)
DEFAULT_FROM_EMAIL: str = avoid_empty_value(
    os.getenv("SCRAPER_DEFAULT_FROM_EMAIL", "scraper@local.dev")
)
ADMIN_EMAIL: str = avoid_empty_value(
    os.getenv("SCRAPER_ADMIN_EMAIL", "admin@local.dev")
)
