# from langgraph.graph import StateGraph,END,START
# from lg_agent.core.state_model import State

# from lg_agent.nodes.intent import intent_classifier
# from lg_agent.nodes.intent_condition_node import intent_condition
# from lg_agent.nodes.new_object_node import create_new_object
# from lg_agent.system.write_files import write_xml_files
# from lg_agent.system.rag import edit_object_rag
# from .assistant_node_client import create_assistant_node
# from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
# from lg_agent.workflow.mcp_tools import get_mcp_tools


# async def build_graph():
#     builder = StateGraph(State)

#     # mcp_tools = get_mcp_tools()

#     mcp_tools = await get_mcp_tools()
#     assistant_node = create_assistant_node(mcp_tools)

#     # Nodes
#     builder.add_node("intent_node", intent_classifier)
#     builder.add_node("intent_condi", intent_condition)
#     builder.add_node("new_object", create_new_object)
#     builder.add_node("rag_node", edit_object_rag)
#     builder.add_node("write_files", write_xml_files)
#     builder.add_node("assistant_node", assistant_node)
#     builder.add_node("tools", ToolNode(mcp_tools))

#     # Edges
#     builder.add_edge(START, "intent_node")
#     builder.add_edge("intent_node", "intent_condi")

#     builder.add_conditional_edges(
#         "intent_condi",
#         lambda state: state["next_node"],
#         {
#             "assistant": "assistant_node",
#             "new_object_node": "new_object",
#             "edit_object_node": "rag_node",
#         },
#     )


#     builder.add_edge("new_object", "write_files")
#     builder.add_edge("write_files", "assistant_node")
#     builder.add_edge("rag_node", "new_object")
#     builder.add_edge("write_files", "assistant_node")
#     builder.add_conditional_edges("assistant_node", tools_condition)
#     builder.add_edge("tools", "assistant_node")

#     builder.add_edge("assistant_node", END)
#     graph = builder.compile(checkpointer=MemorySaver())
#     return graph


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
import copy
import pickle
import asyncio
from psycopg_pool import AsyncConnectionPool
from psycopg.rows import dict_row
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

# Store tools globally
_mcp_tools_cache = None


async def get_cached_mcp_tools():
    global _mcp_tools_cache
    if _mcp_tools_cache is None:
        _mcp_tools_cache = await get_mcp_tools()
    return _mcp_tools_cache


class SafeMemorySaver(MemorySaver):
    """Custom checkpointer that handles unpicklable objects"""

    def _is_safe_type(self, obj):
        """Check if type is safe to preserve"""
        return not isinstance(
            obj, (asyncio.Task, asyncio.Future)
        ) and not asyncio.iscoroutine(obj)

    def _safe_deepcopy(self, obj, memo=None):
        """Safely deep copy objects, skipping unpicklable ones"""
        if memo is None:
            memo = {}

        # Handle already copied objects
        obj_id = id(obj)
        if obj_id in memo:
            return memo[obj_id]

        # Skip unsafe types immediately
        if not self._is_safe_type(obj):
            return None

        # Handle primitives (immutable) - no copy needed
        if isinstance(obj, (str, int, float, bool, type(None), bytes)):
            return obj

        # Handle dictionaries
        if isinstance(obj, dict):
            result = {}
            memo[obj_id] = result
            for key, value in obj.items():
                if self._is_safe_type(key) and self._is_safe_type(value):
                    safe_key = self._safe_deepcopy(key, memo)
                    safe_value = self._safe_deepcopy(value, memo)
                    if safe_key is not None:  # Only add if key is safe
                        result[safe_key] = safe_value
            return result

        # Handle lists
        if isinstance(obj, list):
            result = []
            memo[obj_id] = result
            for item in obj:
                if self._is_safe_type(item):
                    safe_item = self._safe_deepcopy(item, memo)
                    # We keep None in lists to preserve length/indices if needed,
                    # OR we can filter them. Filtering is safer for pickling generally.
                    # But if the logic implies index dependency, this might break.
                    # However, usually state lists in LangChain are history.
                    result.append(safe_item)
            return result

        # Handle tuples
        if isinstance(obj, tuple):
            items = []
            for item in obj:
                if self._is_safe_type(item):
                    items.append(self._safe_deepcopy(item, memo))
            result = tuple(items)
            memo[obj_id] = result
            return result

        # Handle generic objects with __dict__
        if hasattr(obj, "__dict__"):
            try:
                # Create a new instance without calling __init__
                new_obj = obj.__class__.__new__(obj.__class__)
                memo[obj_id] = new_obj

                new_dict = {}
                for k, v in obj.__dict__.items():
                    if self._is_safe_type(v):
                        new_dict[k] = self._safe_deepcopy(v, memo)

                new_obj.__dict__.update(new_dict)
                return new_obj
            except Exception:
                # If we can't reconstruct, fallback to None or string rep check
                pass

        # Fallback to standard deepcopy for other types, catching errors
        try:
            return copy.deepcopy(obj, memo)
        except (TypeError, AttributeError, pickle.PicklingError):
            return None

    def put(self, config, checkpoint, metadata):
        """Store checkpoint with safe copying"""
        try:
            # Create a safe copy of the checkpoint
            safe_checkpoint = self._safe_deepcopy(checkpoint)
            # Ensure return is a valid dict for parent class
            if not isinstance(safe_checkpoint, dict):
                # Fallback if the entire checkpoint got nuked (unlikely)
                safe_checkpoint = {
                    "v": checkpoint.get("v", 1),
                    "ts": checkpoint.get("ts"),
                    "channel_values": {},
                    "channel_versions": checkpoint.get("channel_versions", {}),
                    "versions_seen": checkpoint.get("versions_seen", {}),
                    "pending_sends": [],
                }
            return super().put(config, safe_checkpoint, metadata)
        except Exception as e:
            print(f"⚠️ Checkpoint save warning: {e}")
            # Return a minimal checkpoint
            minimal_checkpoint = {
                "v": checkpoint.get("v", 1),
                "ts": checkpoint.get("ts"),
                "channel_values": {},
                "channel_versions": {},
                "versions_seen": {},
                "pending_sends": [],
            }
            return super().put(config, minimal_checkpoint, metadata)



async def build_graph():
    builder = StateGraph(State)
    # Get tools (cached globally)
    mcp_tools = await get_cached_mcp_tools()

    # Create nodes
    assistant_node = create_assistant_node(mcp_tools)

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

    # Use the safe checkpointer
    graph = builder.compile(checkpointer=MemorySaver())
    return graph
