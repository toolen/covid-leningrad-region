"""This file contains routes and handlers."""
from aiohttp import web


async def districts_handler(request: web.Request) -> web.Response:
    """
    Return list of districts.

    :param request:
    :return:
    """
    districts = request.app["db"].get_districts()
    return web.json_response(districts)


async def district_name_handler(request: web.Request) -> web.Response:
    """
    Return district by name.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    district = request.app["db"].get_district(district_name)
    return web.json_response(district)


async def localities_handler(request: web.Request) -> web.Response:
    """
    Return localities by district name.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    localities = request.app["db"].get_localities(district_name)
    return web.json_response(localities)


async def locality_handler(request: web.Request) -> web.Response:
    """
    Return locality by district and locality names.

    :param request:
    :return:
    """
    district_name = request.match_info["district_name"]
    locality_name = request.match_info["locality_name"]
    locality = request.app["db"].get_locality(district_name, locality_name)
    return web.json_response(locality)


def init_routes(app: web.Application) -> None:
    """
    Initialize application routes.

    :param app:
    :return:
    """
    app.add_routes(
        [
            web.get("/districts", districts_handler),
            web.get("/districts/{district_name}", district_name_handler),
            web.get("/districts/{district_name}/localities", localities_handler),
            web.get(
                "/districts/{district_name}/localities/{locality_name}",
                locality_handler,
            ),
        ]
    )
