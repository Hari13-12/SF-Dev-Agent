from app.core.connect_db import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session 