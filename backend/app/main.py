from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
from app.core.connect_db import async_engine
from app.models.user_details import Base
from sqlalchemy import text

from app.routes import auth_route

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.execute(text("SELECT 1"))
        print("Application startup complete✅")
    except Exception as e:
        print("Failed to start application ",e)
    yield
    print("Application closed successfully")


app = FastAPI(lifespan=lifespan)


app.include_router(auth_route.router)