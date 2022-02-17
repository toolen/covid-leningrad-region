"""This file contains entrypoint of application."""
from typing import Dict, Optional

from aiohttp import web

from dashboard_backend.config import init_config
from dashboard_backend.db import init_db
from dashboard_backend.logging import init_logging
from dashboard_backend.routes import init_routes


def init_app(config: Optional[Dict[str, str]] = None) -> web.Application:
    """
    Initialize application.

    :param config:
    :return:
    """
    app = web.Application()

    init_config(app, override_config=config)
    init_logging(app)
    init_db(app)
    init_routes(app)

    return app


def main() -> None:
    """
    Run application.

    :return:
    """
    app = init_app()
    web.run_app(app)


if __name__ == "__main__":
    main()
