from app.database.session import engine
from app.database.base import Base

async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created/verified")

async def shutdown_event():
    await engine.dispose()
    print("Database connection closed")
