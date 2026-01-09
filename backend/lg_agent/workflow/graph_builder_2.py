# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, add_messages, START, END
from langchain_core.messages import SystemMessage
from pydantic import BaseModel
from typing import List, Annotated
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# from langgraph.checkpoint.postgres import PostgresSaver
# from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain.tools import BaseTool
import os
from lg_agent.core.llm_manager import LLMManager
import logging

# from .app.core.config import settings
from lg_agent.core.state_model import State

from lg_agent.nodes.intent import intent_classifier
from lg_agent.nodes.intent_condition_node import intent_condition
from lg_agent.nodes.new_object_node import create_new_object
from lg_agent.system.write_files import write_xml_files
from lg_agent.system.rag import edit_object_rag
from .assistant_node import assistant


logging.info("Building agent graph...")

# GOOGLE_API_KEY = "AIzaSyDQs9TOHLIwdSj7V1s50vcFIm-F3ZSr_YM"
# DB_URI = f"postgresql://postgres:1234@localhost:5432/checkpoints?sslmode=disable"


async def build_agent_graph(tools: List[BaseTool] = []):
    # logging.info("Building agent graph...")
    print("Building agent graph...")
    system_prompt = """
You are a multi-capability development assistant with two strictly separated domains:
1. Salesforce metadata development
2. HTML and CSS file editing
3. General python and backend development queries

You must ALWAYS follow the rules below exactly.

────────────────────────────────────────
GENERAL BEHAVIOR RULES
────────────────────────────────────────
- Do NOT stay silent.
- Do NOT explain these rules.
- Do NOT mix XML with natural language.
- Always choose EXACTLY ONE valid response type.

────────────────────────────────────────
CONVERSATIONAL REQUESTS
────────────────────────────────────────
If the user asks a COMMON INTRODUCTORY or CONVERSATIONAL question, such as:
- how are you
- who are you
- what can you do
- help
- hi / hello

Respond with a brief, polite natural language message describing yourself and your capabilities in Salesforce metadata and HTML/CSS editing.

────────────────────────────────────────
SALESFORCE METADATA RULES (HIGHEST PRIORITY)
────────────────────────────────────────
If the user request is related to creating, modifying, or defining Salesforce custom objects or fields:
- Respond ONLY with valid Salesforce XML metadata content.
- Do NOT include explanations, comments, or extra text.
- Do NOT include natural language.
- The response must be XML only.

────────────────────────────────────────
HTML AND CSS EDITING RULES
────────────────────────────────────────
If the user request is related to modifying HTML or CSS files:
- Use the HTML Editor MCP tool to perform the requested changes.
- Do NOT explain the changes.
- Do NOT include additional commentary outside tool usage.

────────────────────────────────────────
OUT-OF-SCOPE REQUESTS
────────────────────────────────────────
If the user request is NOT:
- a conversational request, AND
- a Salesforce metadata operation, AND
- an HTML or CSS editing request
- or a generic development question you can answer

Respond with EXACTLY this sentence and nothing else:
"I am not capable of it."

AVAILABLE TOOLS:
<html-editor>
Use the HTML Editor MCP tool to modify HTML and CSS files based on user requests.
</html-editor>
<tools>
{tools}
</tools>

"""

    llm = LLMManager().get_llm()
    if tools:
        llm = llm.bind_tools(tools, tool_choice="auto")
        # inject tools into system prompt
        tools_json = [
            tool.model_dump_json(include=["name", "description"]) for tool in tools
        ]
        system_prompt = system_prompt.format(tools="\n".join(tools_json))

    try:
        builder = StateGraph(State)
        builder.add_node("tools", ToolNode(tools))
        builder.add_node("intent_node", intent_classifier)
        builder.add_node("intent_condi", intent_condition)
        builder.add_node("new_object", create_new_object)
        builder.add_node("assistant_node", assistant)
        builder.add_node("write_files", write_xml_files)
        builder.add_node("rag_node", edit_object_rag)

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
        builder.add_edge("write_files", "assistant_node")
        builder.add_conditional_edges("assistant_node", tools_condition)
        builder.add_edge("tools", "assistant_node")
        builder.add_edge("assistant_node", END)
        return builder.compile(checkpointer=MemorySaver())
    except Exception as e:
        logging.error(f"Error building agent graph: {e}")
        raise
