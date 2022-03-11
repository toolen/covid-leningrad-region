"""This file contains CORS methods."""
import aiohttp_cors
from aiohttp import web
from aiohttp_cors import ResourceOptions

CORS_DEFAULT_HEADERS = (
    "Host",
    "User-Agent",
    "Accept",
    "Accept-Language",
    "Accept-Encoding",
    "Access-Control-Request-Method",
    "Access-Control-Request-Headers",
    "Origin",
    "Connection",
    "Pragma",
    "Cache-Control",
    "Content-Type",
)

CORS_DEFAULT_METHODS = (
    "GET",
    "OPTIONS",
)


def init_cors(app: web.Application) -> None:
    """
    Initialize application with CORS.

    :param web.Application app: instance of application.
    :return: None
    """
    cors_origin = app["config"]["CORS_ORIGIN"]
    cors = aiohttp_cors.setup(
        app,
        defaults={
            cors_origin: ResourceOptions(
                allow_headers=CORS_DEFAULT_HEADERS, allow_methods=CORS_DEFAULT_METHODS
            )
        },
    )
    for route in list(app.router.routes()):
        cors.add(route)
