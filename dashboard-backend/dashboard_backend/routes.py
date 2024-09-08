"""This file contains routes and handlers."""

from aiohttp import web

from dashboard_backend.encoders import mongo_dumps


async def health_handler(request: web.Request) -> web.Response:
    """
    Return healthcheck response.

    :return: Response
    """
    return web.json_response({"health": "ok"})


async def districts_handler(request: web.Request) -> web.Response:
    """
    Return list of districts.

    :param request:
    :return:
    """
    districts = await request.app["db"].get_districts()
    return web.json_response(districts)


async def district_name_handler(request: web.Request) -> web.Response:
    """
    Return district by name.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    district = await request.app["db"].get_district(district_name)
    return web.json_response(district)


async def localities_handler(request: web.Request) -> web.Response:
    """
    Return localities by district name.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    localities = await request.app["db"].get_localities(district_name)
    return web.json_response(localities)


async def locality_handler(request: web.Request) -> web.Response:
    """
    Return locality by district and locality names.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    locality_name = request.match_info["locality_name"]
    locality = await request.app["db"].get_locality(district_name, locality_name)
    return web.json_response(locality, dumps=mongo_dumps)


def init_routes(app: web.Application) -> None:
    """
    Initialize application routes.

    :param app:
    :return:
    """
    app.add_routes(
        [
            web.get("/api/v1/health", health_handler, name="health"),
            web.get("/api/v1/districts", districts_handler),
            web.get("/api/v1/districts/{district_name}", district_name_handler),
            web.get("/api/v1/districts/{district_name}/localities", localities_handler),
            web.get(
                "/api/v1/districts/{district_name}/localities/{locality_name}",
                locality_handler,
            ),
        ]
    )
