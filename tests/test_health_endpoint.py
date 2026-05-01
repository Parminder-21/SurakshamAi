import asyncio
from httpx import ASGITransport, AsyncClient

from main import app

async def _fetch_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.get("/health")


def test_health_endpoint_returns_ok_status():
    response = asyncio.run(_fetch_health())

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
