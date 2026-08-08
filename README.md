# TravelBudget AI - FastAPI Backend

Production-ready backend for AI-Powered Travel & Budget Manager.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
cp .env.example .env

# 4. Run the server
uvicorn app.main:app --reload --port 8000

# 5. Open API docs
http://localhost:8000/api/docs
```

## API Endpoints

- POST /api/v1/auth/register - User registration
- POST /api/v1/auth/login - User login (returns JWT)
- GET /api/v1/auth/me - Get current user
- POST /api/v1/auth/refresh - Refresh access token
- CRUD /api/v1/trips - Trip management
- CRUD /api/v1/expenses - Expense tracking
- GET/PUT /api/v1/budget/trip/{id} - Budget allocation
- POST /api/v1/budget/recommend - AI budget recommendation
- POST /api/v1/ai/plan-trip - AI trip planner
- POST /api/v1/ai/packing-list - Smart packing list
- GET /api/v1/weather/current/{city} - Weather data
- GET /api/v1/currency/convert - Currency conversion
- GET /api/v1/notifications - User notifications
- CRUD /api/v1/journals - Travel journal
- GET /api/v1/admin/dashboard - Admin dashboard
