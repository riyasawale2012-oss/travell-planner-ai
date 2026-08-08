import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_create_trip_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/v1/trips", json={
            "source": "Mumbai", "destination": "Goa",
            "start_date": "2024-09-01", "end_date": "2024-09-05",
            "total_budget": 15000, "num_travellers": 2
        })
        assert response.status_code in [401, 403]
