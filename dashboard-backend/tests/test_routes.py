from aiohttp import web

from dashboard_backend.routes import init_routes


async def test_health_handler(aiohttp_client):
    app = web.Application()
    init_routes(app)
    client = await aiohttp_client(app)
    url = client.app.router["health"].url_for()
    result = await client.get(url)

    assert result.status == 200

    data = await result.json()
    assert data.get("health") == "ok"
