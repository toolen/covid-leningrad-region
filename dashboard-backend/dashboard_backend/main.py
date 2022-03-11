"""This file contains entrypoint of application."""
import argparse
import logging
import sys
from typing import Dict, Optional

from aiohttp import web

from dashboard_backend.config import init_config
from dashboard_backend.cors import init_cors
from dashboard_backend.db import init_db
from dashboard_backend.routes import init_routes

parser = argparse.ArgumentParser()
parser.add_argument("--host", default="127.0.0.1")
parser.add_argument("--port", default=8080)


def init_logging(app: web.Application) -> None:
    """
    Initialize application logging.

    :param app: application instance.
    :return: None
    """
    log_level = app["config"]["LOG_LEVEL"]
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
        stream=sys.stdout,
    )


def init_app(config: Optional[Dict[str, str]] = None) -> web.Application:
    """
    Initialize application.

    :param config: dictionary.
    :return: application instance.
    """
    app = web.Application()

    init_config(app, override_config=config)
    init_logging(app)
    init_db(app)
    init_routes(app)
    if app["config"]["CORS_ENABLED"]:
        init_cors(app)

    return app


def main() -> None:
    """
    Run application.

    :return: None
    """
    app = init_app()
    args = parser.parse_args()
    web.run_app(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
