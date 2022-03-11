"""This file contains config methods."""
import os
from typing import Dict, Optional, Union

from aiohttp import web

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CERTS_DIR = os.path.join(BASE_DIR, "certs")

env = os.environ


def get_config(
    override_config: Optional[Dict[str, str]] = None
) -> Dict[str, Union[str, bool]]:
    """
    Return application configuration.

    :param override_config: dict to override initial configuration.
    :return: None
    """
    default_tls_cert_key_path = f"{CERTS_DIR}/dashboard.pem"
    if not os.path.exists(default_tls_cert_key_path):
        default_tls_cert_key_path = ""

    default_ca_path = f"{CERTS_DIR}/ca.pem"
    if not os.path.exists(default_ca_path):
        default_ca_path = ""

    config = {
        "DB_URI": os.getenv(
            "DASHBOARD_BACKEND_DB_URI",
            "mongodb://localhost:27017/?authSource=%24external&authMechanism=MONGODB-X509",
        ),
        "DB_NAME": os.getenv("DASHBOARD_BACKEND_DB_NAME", "covid_stat"),
        "DB_COLLECTION_NAME": os.getenv(
            "DASHBOARD_BACKEND_DB_COLLECTION_NAME", "leningrad_region"
        ),
        "TLS_CERT_KEY_PATH": os.getenv(
            "DASHBOARD_BACKEND_TLS_CERT_KEY_PATH", default_tls_cert_key_path
        ),
        "TLS_CA_PATH": os.getenv("DASHBOARD_BACKEND_TLS_CA_PATH", default_ca_path),
        "LOG_LEVEL": os.getenv("DASHBOARD_BACKEND_LOG_LEVEL", "DEBUG"),
        "CORS_ENABLED": os.getenv("DASHBOARD_BACKEND_CORS_ENABLED", True),
        "CORS_ORIGIN": os.getenv("DASHBOARD_BACKEND_CORS_ORIGIN", "*"),
    }

    if override_config:
        config.update(override_config)

    return config


def init_config(
    app: web.Application, override_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Initialize application configuration.

    :param app: application instance.
    :param override_config: dictionary that override config.
    :return: None
    """
    config = get_config(override_config)
    app["config"] = config
