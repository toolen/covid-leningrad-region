from typing import Optional, Dict

from aiohttp import web

from dashboard_backend.config import init_config
from dashboard_backend.db import init_db
from dashboard_backend.routes import init_routes


def init_app(config: Optional[Dict[str, str]] = None) -> web.Application:
    app = web.Application()

    init_config(app, override_config=config)
    init_db(app)
    init_routes(app)

    return app
