from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from contextlib import asynccontextmanager
from app.core.connect_db import async_engine
from app.models.user_details import Base
from sqlalchemy import text
from app.routes import auth_route

from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent
from langgraph.checkpoint.memory import InMemorySaver

from lg_agent.workflow.graph_builder import builder

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

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

app.include_router(auth_route.router)

add_langgraph_fastapi_endpoint(
  app=app,
  agent=LangGraphAGUIAgent(
    name="sample_agent",
    description="An example agent to use as a starting point for your own agent.",
    graph=graph,
  ),
  path="/agent",
)