from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, trips, expenses, budget, ai, weather, currency, notifications, journals, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(trips.router, prefix="/trips", tags=["Trips"])
api_router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
api_router.include_router(budget.router, prefix="/budget", tags=["Budget"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI Planner"])
api_router.include_router(weather.router, prefix="/weather", tags=["Weather"])
api_router.include_router(currency.router, prefix="/currency", tags=["Currency"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
api_router.include_router(journals.router, prefix="/journals", tags=["Travel Journal"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
