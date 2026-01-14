# import asyncio
# import sys

# if sys.platform == 'win32':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from fastapi import FastAPI


from copilotkit import LangGraphAGUIAgent 
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from lg_agent.workflow.graph_builder_client_2 import build_graph
# from lg_agent.workflow.post_memory import init_checkpointe  
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn


graph = None


# async def get_graph():
#     return await build_graph()
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global graph
#     # await get_mcp_tools()
#     # graph = await build_graph()   # ✅ compiled graph
#     yield
# app = FastAPI(lifespan = lifespan) 

# agent_instance = LangGraphAGUIAgent(
#     name="sample_agent",
#     description="Salesforce MCP Agent",
#     graph= get_graph # Lazy build
# )

# add_langgraph_fastapi_endpoint(app=app, agent=agent_instance, path="/")

# if __name__ == "__main__":
#     uvicorn.run(
#         "lg_agent.main_app_1:app",
#         host="127.0.0.1",
#         port=8000,
#     )



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global graph, agent_instance
    
    # Build the graph first (this is async and awaited)
    graph = await build_graph()
    print("✅ LangGraph built and ready")
    
    # Create agent instance after graph is ready
    agent_instance = LangGraphAGUIAgent(
        name="sample_agent",
        description="Describe your agent here, will be used for multi-agent orchestration",
        graph=graph,  # Pass the actual graph object
    )
    
    # Add the endpoint with the initialized agent
    add_langgraph_fastapi_endpoint(
        app=app,
        agent=agent_instance,
        path="/",
    )
    print("✅ Endpoint added")
    
    yield
    
    # Shutdown (if needed)
    print("🔻 Shutting down...")

app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "lg_agent.main_app_1:app",
        host="127.0.0.1",
        port=8000,
    )

