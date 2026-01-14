# import os
# from fastapi import FastAPI
# import uvicorn
# from copilotkit import LangGraphAGUIAgent 
# from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
# from samagent import agent
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi import Request
# from fastapi.responses import JSONResponse
# import uuid

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

# # Health check
# @app.get("/health")
# def health():
#     """Health check."""
#     return {"status": "ok"}

# # Assistants search endpoint
# @app.post("/agent/assistants/search")
# async def search_assistants(request: Request):
#     """Required endpoint for CopilotKit to discover the agent"""
#     return JSONResponse([{
#         "assistant_id": "sample_agent",
#         "name": "Sample Agent",
#         "graph_id": "sample_agent",
#         "model": "sample_agent",
#         "metadata": {
#             "name": "sample_agent",
#             "description": "Describe your agent here"
#         }
#     }])

# # Agent info endpoint
# @app.get("/agent/info")
# async def agent_info():
#     """Agent info endpoint"""
#     return JSONResponse({
#         "name": "sample_agent",
#         "description": "Describe your agent here",
#         "capabilities": []
#     })

# # Threads endpoint - create a new thread
# @app.post("/agent/threads")
# async def create_thread(request: Request):
#     """Create a new conversation thread"""
#     thread_id = str(uuid.uuid4())
#     return JSONResponse({
#         "thread_id": thread_id,
#         "created_at": "2024-01-01T00:00:00Z",
#         "metadata": {}
#     })

# # Get thread by ID
# @app.get("/agent/threads/{thread_id}")
# async def get_thread(thread_id: str):
#     """Get a specific thread"""
#     return JSONResponse({
#         "thread_id": thread_id,
#         "created_at": "2024-01-01T00:00:00Z",
#         "metadata": {}
#     })

# def main():
#     """Run the uvicorn server."""
#     port = int(os.getenv("PORT", "8000"))
#     uvicorn.run(
#         "sampleagent.main2:app", 
#         host="127.0.0.1",
#         port=port,
#         reload=True,
#     )


import os
from fastapi import FastAPI, Request, HTTPException
import uvicorn
from copilotkit import LangGraphAGUIAgent 
from ag_ui_langgraph import add_langgraph_fastapi_endpoint 
from samagent import agent
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import uuid
import json
from datetime import datetime

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

# Store for threads (in-memory, for development)
threads_store = {}

# Add LangGraph endpoint
add_langgraph_fastapi_endpoint(
  app=app,
  agent=LangGraphAGUIAgent(
    name="sample_agent", 
    description="A helpful AI agent for development tasks",
    graph=agent, 
  ),
  path="/agent", 
)

# Health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}

# Assistants search endpoint
@app.post("/agent/assistants/search")
async def search_assistants(request: Request):
    """Search for available assistants"""
    try:
        body = await request.json()
        print(f"Assistants search request: {body}")
    except:
        pass
    
    return [{
        "assistant_id": "sample_agent",
        "name": "Sample Agent",
        "graph_id": "sample_agent",
        "model": "sample_agent",
        "metadata": {
            "name": "sample_agent",
            "description": "A helpful AI agent for development tasks"
        }
    }]

# Agent info endpoint
@app.get("/agent/info")
async def agent_info():
    """Get agent information"""
    return {
        "name": "sample_agent",
        "description": "A helpful AI agent for development tasks",
        "capabilities": []
    }

# Create thread
@app.post("/agent/threads")
async def create_thread(request: Request):
    """Create a new conversation thread"""
    try:
        body = await request.json()
        print(f"Create thread request: {body}")
    except Exception as e:
        print(f"Error parsing request body: {e}")
        body = {}
    
    thread_id = str(uuid.uuid4())
    thread_data = {
        "thread_id": thread_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "metadata": body.get("metadata", {})
    }
    threads_store[thread_id] = thread_data
    
    return thread_data

# Get thread
@app.get("/agent/threads/{thread_id}")
async def get_thread(thread_id: str):
    """Get a specific thread"""
    if thread_id in threads_store:
        return threads_store[thread_id]
    
    # Return a default thread if not found (for development)
    return {
        "thread_id": thread_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "metadata": {}
    }

# Run agent (streaming)
@app.post("/agent/threads/{thread_id}/runs")
async def create_run(thread_id: str, request: Request):
    """Create a run for the thread"""
    try:
        body = await request.json()
        print(f"Run request for thread {thread_id}: {body}")
        
        # Return a run ID
        run_id = str(uuid.uuid4())
        return {
            "run_id": run_id,
            "thread_id": thread_id,
            "status": "queued",
            "created_at": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        print(f"Error in create_run: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Add a catch-all for debugging
@app.api_route("/agent/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(path: str, request: Request):
    """Catch-all route to log all requests"""
    print(f"Unhandled request: {request.method} /agent/{path}")
    try:
        body = await request.json()
        print(f"Request body: {body}")
    except:
        pass
    
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Endpoint /agent/{path} not found",
            "method": request.method,
            "available_endpoints": [
                "/agent/assistants/search",
                "/agent/info",
                "/agent/threads",
                "/agent/threads/{thread_id}",
                "/agent/threads/{thread_id}/runs"
            ]
        }
    )

def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "sampleagent.main2:app", 
        host="127.0.0.1",
        port=port,
        reload=True,
    )

if __name__ == "__main__":
    main()