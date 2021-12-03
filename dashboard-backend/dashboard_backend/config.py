"""This file contains config methods."""
import os
from typing import Dict, Optional

from aiohttp import web

env = os.environ


def init_config(
        app: web.Application, override_config: Optional[Dict[str, str]] = None
) -> None:
    """
    Initialize application configuration.
    :param app:
    :param override_config:
    :return:
    """
    config = {
        'DB_URI': os.getenv('BACKEND_DB_URI', 'mongodb://localhost:27017'),
        'DB_NAME': os.getenv('BACKEND_DB_NAME', 'covid_stat'),
        'DB_COLLECTION_NAME': os.getenv('BACKEND_DB_COLLECTION_NAME', 'leningrad_region'),
        'TLS_CERT_KEY_PATH': os.getenv('BACKEND_TLS_CERT_KEY_PATH'),
        'TLS_CA_PATH': os.getenv('BACKEND_TLS_CA_PATH'),
    }
    if override_config:
        config.update(override_config)
    app['config'] = config
