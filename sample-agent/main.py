# import os
# from fastapi import FastAPI
# import uvicorn
# from copilotkit import LangGraphAGUIAgent 
# from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
# from samagent import agent
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import Request
# from fastapi.responses import JSONResponse

# from dotenv import load_dotenv
# load_dotenv()
# app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# add_langgraph_fastapi_endpoint(
#   app=app,
#   agent=LangGraphAGUIAgent(
#     name="sample_agent", 
#     description="Describe your agent here, will be used for multi-agent orchestration",
#     graph=agent, 
#   ),
#   path="/agent", 
# )

# # add new route for health check
# @app.get("/health")
# def health():
#     """Health check."""
#     return {"status": "ok"}


# def main():
#     """Run the uvicorn server."""
#     port = int(os.getenv("PORT", "8000"))
#     uvicorn.run(
#         "sampleagent.main:app", 
#         host="127.0.0.1",
#         port=port,
#         reload=True,
#     )


import os
from fastapi import FastAPI
import uvicorn
from copilotkit import LangGraphAGUIAgent 
from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
from samagent import agent
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_langgraph_fastapi_endpoint(
  app=app,
  agent=LangGraphAGUIAgent(
    name="sample_agent", 
    description="Describe your agent here, will be used for multi-agent orchestration",
    graph=agent, 
  ),
  path="/agent", 
)

# Health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

# Add the assistants search endpoint that CopilotKit expects
@app.post("/agent/assistants/search")
async def search_assistants(request: Request):
    """Required endpoint for CopilotKit to discover the agent"""
    return JSONResponse([{  # ← Return an ARRAY, not an object with "assistants" key
        "assistant_id": "sample_agent",
        "name": "Sample Agent",
        "graph_id": "sample_agent",
        "model": "sample_agent",
        "metadata": {
            "name": "sample_agent",
            "description": "Describe your agent here"
        }
    }])

# Add the info endpoint
@app.get("/agent/info")
async def agent_info():
    """Agent info endpoint"""
    return JSONResponse({
        "name": "sample_agent",
        "description": "Describe your agent here",
        "capabilities": []
    })

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "sampleagent.main:app", 
        host="127.0.0.1",
        port=port,
        reload=True,
    )