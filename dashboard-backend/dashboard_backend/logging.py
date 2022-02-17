"""This files contains logging configuration methods."""
import logging
import sys

from aiohttp import web


def init_logging(app: web.Application) -> None:
    """
    Initialize application logging.

    :param app: application instance
    :return: None
    """
    log_level = app["config"]["LOG_LEVEL"]
    logging.basicConfig(
        level=log_level,
        format="[%(levelname)s %(asctime)s %(name)s] %(message)s",
        stream=sys.stdout,
    )
