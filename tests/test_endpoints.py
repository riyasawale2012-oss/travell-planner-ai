import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_full_user_flow_and_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

        # 2. Root endpoint
        res = await client.get("/")
        assert res.status_code == 200

        # 3. Register user
        reg_data = {
            "full_name": "John Doe",
            "email": "johndoe@example.com",
            "password": "SecurePassword123!",
            "phone": "+1234567890"
        }
        res = await client.post("/api/v1/auth/register", json=reg_data)
        assert res.status_code == 201
        user_info = res.json()
        assert user_info["email"] == "johndoe@example.com"

        # 4. Login user
        login_res = await client.post("/api/v1/auth/login", json={"email": "johndoe@example.com", "password": "SecurePassword123!"})
        assert login_res.status_code == 200
        tokens = login_res.json()
        token = tokens["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 5. Get Profile
        profile_res = await client.get("/api/v1/users/profile", headers=headers)
        assert profile_res.status_code == 200
        assert profile_res.json()["email"] == "johndoe@example.com"
        assert profile_res.json()["total_trips"] == 0

        # 6. Create Trip
        trip_data = {
            "source": "Mumbai",
            "destination": "Goa",
            "start_date": "2026-09-01",
            "end_date": "2026-09-07",
            "total_budget": 20000.0,
            "currency": "INR",
            "num_travellers": 2,
            "travel_style": "moderate"
        }
        trip_res = await client.post("/api/v1/trips", json=trip_data, headers=headers)
        assert trip_res.status_code == 201
        trip = trip_res.json()
        trip_id = trip["trip_id"]

        # 7. List Trips
        list_trips_res = await client.get("/api/v1/trips", headers=headers)
        assert list_trips_res.status_code == 200
        assert list_trips_res.json()["total"] == 1

        # 8. Create Expense
        exp_data = {
            "trip_id": trip_id,
            "amount": 2500.0,
            "currency": "INR",
            "category": "food",
            "description": "Seafood dinner",
            "expense_date": "2026-09-02T19:00:00Z"
        }
        exp_res = await client.post("/api/v1/expenses", json=exp_data, headers=headers)
        assert exp_res.status_code == 201
        exp_id = exp_res.json()["expense_id"]

        # 9. Get Expense Summary
        exp_sum_res = await client.get(f"/api/v1/expenses/trip/{trip_id}/summary", headers=headers)
        assert exp_sum_res.status_code == 200
        assert exp_sum_res.json()["total_spent"] == 2500.0

        # 10. AI Plan Trip
        plan_req = {
            "current_city": "Mumbai",
            "destination": "Goa",
            "is_international": False,
            "start_date": "2026-09-01",
            "end_date": "2026-09-07",
            "budget": 20000.0,
            "num_travellers": 2,
            "travel_style": "moderate"
        }
        ai_res = await client.post("/api/v1/ai/plan-trip", json=plan_req, headers=headers)
        assert ai_res.status_code == 200
        assert "itinerary" in ai_res.json()

        # 11. Weather Current
        w_res = await client.get("/api/v1/weather/current/Goa", headers=headers)
        assert w_res.status_code == 200
        assert w_res.json()["city"] == "Goa"

        # 12. Currency Rates
        c_res = await client.get("/api/v1/currency/rate?from_currency=INR&to_currency=USD", headers=headers)
        assert c_res.status_code == 200

        # 13. Create Journal
        j_data = {
            "trip_id": trip_id,
            "title": "First day in Goa!",
            "content": "Had an amazing sunset view at Baga Beach.",
            "photos": ["https://example.com/photo1.jpg"],
            "mood": "excited",
            "rating": 5.0
        }
        j_res = await client.post("/api/v1/journals", json=j_data, headers=headers)
        assert j_res.status_code == 201
        assert j_res.json()["photos"] == ["https://example.com/photo1.jpg"]

        # 14. Get Notifications
        n_res = await client.get("/api/v1/notifications", headers=headers)
        assert n_res.status_code == 200
