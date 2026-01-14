# # # import os
# # # from fastapi import FastAPI
# # # import uvicorn
# # # from copilotkit import LangGraphAGUIAgent 
# # # from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
# # # from lg_agent.workflow.graph_builder_client import build_graph
# # # from lg_agent.workflow.mcp_tools import get_mcp_tools




# # # graph = None


# # # app = FastAPI()


# # # @app.on_event("startup")
# # # async def startup():
# # #     global graph

# # #     # 1️⃣ Initialize MCP tools FIRST
# # #     await get_mcp_tools()
# # #     print("✅ MCP tools initialized")

# # #     # 2️⃣ Build graph AFTER tools exist
# # #     graph = build_graph()
# # #     print("✅ LangGraph built")





# # # add_langgraph_fastapi_endpoint(
# # #     app=app,
# # #     agent=LangGraphAGUIAgent(
# # #         name="sample_agent",
# # #         description="Describe your agent here, will be used for multi-agent orchestration",
# # #         graph=lambda: graph,   # 🔑 LAZY RESOLUTION
# # #     ),
# # #     path="/",
# # # )


# # # if __name__ == "__main__":
# # #     uvicorn.run(app, host="127.0.0.1", port=8000)



# # from fastapi import FastAPI
# # import uvicorn
# # from copilotkit import LangGraphAGUIAgent
# # from ag_ui_langgraph import add_langgraph_fastapi_endpoint
# # from lg_agent.workflow.graph_builder_client import build_graph
 
# # builder = build_graph()
 
 
# # app = FastAPI()
 
# # add_langgraph_fastapi_endpoint(
# #   app=app,
# #   agent=LangGraphAGUIAgent(
# #     name="sample_agent",
# #     description="Describe your agent here, will be used for multi-agent orchestration",
# #     graph=builder,
# #   ),
# #   path="/",
# # )
 
# # if __name__ == "__main__":
# #     uvicorn.run(app, host="127.0.0.1", port=8000)
 

# from fastapi import FastAPI
# import uvicorn
# from copilotkit import LangGraphAGUIAgent
# from ag_ui_langgraph import add_langgraph_fastapi_endpoint
# from lg_agent.workflow.graph_builder_client import build_graph

# app = FastAPI()
# graph = None

# @app.on_event("startup")
# async def startup():
#     global graph
#     # Await the async build_graph function
#     graph = await build_graph()
#     print("✅ LangGraph built and ready")

# add_langgraph_fastapi_endpoint(
#     app=app,
#     agent=LangGraphAGUIAgent(
#         name="sample_agent",
#         description="Describe your agent here, will be used for multi-agent orchestration",
#         graph=lambda: graph,  # Use lambda for lazy resolution
#     ),
#     path="/",
# )

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)



# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# import uvicorn
# from copilotkit import LangGraphAGUIAgent
# from ag_ui_langgraph import add_langgraph_fastapi_endpoint
# from lg_agent.workflow.graph_builder_client import build_graph

# graph = None

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     global graph
#     graph = await build_graph()
#     print("✅ LangGraph built and ready")
#     yield
#     # Shutdown (if needed)
#     print("🔻 Shutting down...")

# app = FastAPI(lifespan=lifespan)

# add_langgraph_fastapi_endpoint(
#     app=app,
#     agent=LangGraphAGUIAgent(
#         name="sample_agent",
#         description="Describe your agent here, will be used for multi-agent orchestration",
#         graph=lambda: graph,
#     ),
#     path="/",
# )

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)

# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# import uvicorn
# from copilotkit import LangGraphAGUIAgent
# from ag_ui_langgraph import add_langgraph_fastapi_endpoint
# from lg_agent.workflow.graph_builder_client import build_graph

# # Global variables
# graph = None
# agent_instance = None

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup
#     global graph, agent_instance
    
#     # Build the graph first
#     graph = await build_graph()
#     print("✅ LangGraph built and ready")
    
    # Create agent instance after graph is ready
    # agent_instance = LangGraphAGUIAgent(
    #     name="sample_agent",
    #     description="Describe your agent here, will be used for multi-agent orchestration",
    #     graph=graph,  # Pass the actual graph object, not a lambda
    # )
    
    # Now add the endpoint with the initialized agent
    # add_langgraph_fastapi_endpoint(
    #     app=app,
    #     agent=agent_instance,
    #     path="/",
    # )
    # print("✅ Endpoint added")
    
    # yield
    
    # Shutdown (if needed)
    # print("🔻 Shutting down...")

# app = FastAPI(lifespan=lifespan)

# if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)


import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from copilotkit import LangGraphAGUIAgent
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from lg_agent.workflow.graph_builder_client_2 import build_graph

# Global variables
graph = None
agent_instance = None

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

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)

