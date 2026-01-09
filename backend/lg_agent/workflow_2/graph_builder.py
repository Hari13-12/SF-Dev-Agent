# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, add_messages, START
from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from typing import List, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.postgres import PostgresSaver 
# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver 
from langchain.tools import BaseTool
import os
import logging
from lg_agent.core.llm_manager import LLMManager as LLMManager
# from .app.core.config import settings


logging.info("Building agent graph...")

class AgentState(BaseModel):
    messages: Annotated[List, add_messages]
    file_name: List[str] = []


async def sub_graph(tools: List[BaseTool] = []):
    logging.info("Building agent graph...")
    system_prompt = """
You are Scout, an HTML and CSS editor assistant. Your job is to modify HTML and CSS files based on user requests.

AVAILABLE TOOLS:

<html-editor>
Use the HTML Editor MCP tool to modify HTML and CSS files based on user requests.
</html-editor>

<tools>
{tools}
</tools>

"""
    llm = LLMManager()
    
    if tools:
        llm = llm.bind_tools(tools)
        #inject tools into system prompt
        tools_json = [tool.model_dump_json(include=["name", "description"]) for tool in tools]
        system_prompt = system_prompt.format(
            tools="\n".join(tools_json)
            )

    def assistant(state: AgentState) -> AgentState:
        # Build context message with file paths
        context = ""
        if state.file_name:
            context = "\n\nFILE PATHS AVAILABLE:\n"
            for i, file_path in enumerate(state.file_name):
                if file_path.endswith('.html'):
                    context += f"- HTML file: {file_path}\n"
                elif file_path.endswith('.css'):
                    context += f"- CSS file: {file_path}\n"
        
        # Invoke LLM with the system prompt and file context
        response = llm.invoke([SystemMessage(content=system_prompt + context)] + state.messages)
        state.messages.append(response)
        return state
    try:
        builder = StateGraph(AgentState)
        builder.add_node("Scout", assistant)
        builder.add_node(ToolNode(tools))

        builder.add_edge(START, "Scout")
        builder.add_conditional_edges("Scout", tools_condition)
        builder.add_edge("tools", "Scout")
        
        # checkpointer = AsyncPostgresSaver.from_conn_string(DB_URI)
        # return builder.compile(checkpointer=checkpointer)
        return builder.compile(checkpointer=MemorySaver())
    except Exception as e:
        logging.error(f"Error building agent graph: {e}")
        raise

