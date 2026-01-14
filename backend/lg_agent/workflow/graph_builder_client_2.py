from langgraph.graph import StateGraph, END, START
from lg_agent.core.state_model import State
from lg_agent.nodes.intent import intent_classifier
from lg_agent.nodes.intent_condition_node import intent_condition
from lg_agent.nodes.new_object_node import create_new_object
from lg_agent.system.write_files import write_xml_files
from lg_agent.system.rag import edit_object_rag
from .assistant_node_client import create_assistant_node
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from lg_agent.workflow.mcp_tools import get_mcp_tools
# from lg_agent.workflow.mcp_tools2 import get_structured_mcp_tools
import copy
import pickle
import asyncio
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import psycopg



async def initialize():
    try:
        conn_string = "postgresql://postgres:1234@localhost:5432/sqlagentcheckpoint"
        conn = await psycopg.AsyncConnection.connect(conn_string, autocommit=True)
        memory = AsyncPostgresSaver(conn)
        await memory.setup()
        print("Memory initialized")
        return memory
    except Exception as e:
        print("Error while creating memory", str(e))
        return None



async def build_graph():
    print("Inside build graph")
    builder = StateGraph(State)
    # Get tools (cached globally)
    print("MCP tools called")
    # mcp_tools = await get_structured_mcp_tools()
    mcp_tools = await get_mcp_tools()
    print("MCP tools done")
    # Create nodes
    print("Before Assistant")
    assistant_node = create_assistant_node(mcp_tools)
    print("After assistant")
    print("Before Memory")
    memory = await initialize()
    print("After memory")
    # Add nodes
    builder.add_node("intent_node", intent_classifier)
    builder.add_node("intent_condi", intent_condition)
    builder.add_node("new_object", create_new_object)
    builder.add_node("rag_node", edit_object_rag)
    builder.add_node("write_files", write_xml_files)
    builder.add_node("assistant_node", assistant_node)
    builder.add_node("tools", ToolNode(mcp_tools))

    # Add edges
    builder.add_edge(START, "intent_node")
    builder.add_edge("intent_node", "intent_condi")

    builder.add_conditional_edges(
        "intent_condi",
        lambda state: state["next_node"],
        {
            "assistant": "assistant_node",
            "new_object_node": "new_object",
            "edit_object_node": "rag_node",
        },
    )

    builder.add_edge("new_object", "write_files")
    builder.add_edge("write_files", "assistant_node")
    builder.add_edge("rag_node", "new_object")
    builder.add_conditional_edges("assistant_node", tools_condition)
    builder.add_edge("tools", "assistant_node")
    builder.add_edge("assistant_node", END)
    graph = builder.compile(checkpointer = MemorySaver())
    return graph

    
