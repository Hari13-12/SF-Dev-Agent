from langgraph.graph import StateGraph,END,START
from lg_agent.core.state_model import State

from lg_agent.nodes.intent import intent_classifier
from lg_agent.nodes.intent_condition_node import intent_condition
from lg_agent.nodes.new_object_node import create_new_object
from lg_agent.system.write_files import write_xml_files
from lg_agent.system.rag import edit_object_rag
from .assistant_node import assistant

builder = StateGraph(State)

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
    lambda state: state["next_node"],{
        "assistant" : "assistant_node",
        "new_object_node" : "new_object",
        "edit_object_node" : "rag_node"
    }
)
builder.add_edge("new_object", "write_files")
builder.add_edge("write_files", "assistant_node")
builder.add_edge("rag_node", "new_object")
builder.add_edge("write_files", "assistant_node")
builder.add_edge("assistant_node", END)
print("Graph builder")
