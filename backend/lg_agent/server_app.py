import os
from fastapi import FastAPI
import uvicorn
from lg_agent.workflow.graph_builder_client import build_graph
from langchain_core.messages import HumanMessage




async def get_graph():
    return await build_graph()


app = FastAPI()


@app.post("/query")
async def main(user_query: str):
    graph = await get_graph()
    graph_config = {
            "configurable": {
                "thread_id": "1"
            }
        }
    input_message = [HumanMessage(content=user_query)]
    output_message = await graph.ainvoke({'messages': input_message}, config = graph_config)  # Remove await here

    return output_message["messages"]