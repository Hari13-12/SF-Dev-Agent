"""
This file implements the MCP Client for our Langgraph Agent.

MCP Clients are responsible for connecting and communicating with MCP servers. 
This client is analagous to Cursor or Claude Desktop and you would configure them in the 
same way by specifying the MCP server configuration in my_mcp/mcp_config.json.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessageChunk
from typing import AsyncGenerator
from lg_agent.workflow.graph_builder_3 import build_agent_graph
from lg_agent.core.state_model import State
import traceback

async def stream_graph_response(
        input: State, graph: StateGraph, config: dict = {}, file_name: list = []
        ) -> AsyncGenerator[str, None]:
    """
    Stream the response from the graph while parsing out tool calls.

    Args:
        input: The input for the graph.
        graph: The graph to run.
        config: The config to pass to the graph. Required for memory.
        file_name: List of file names to pass to the agent.

    Yields:
        A processed string from the graph's chunked response.
    """
    # Add file_name to the input state
    # input.file_name = file_name
    
    async for message_chunk, metadata in graph.astream(
        input=input,
        stream_mode="messages",
        config=config
        ):
        if isinstance(message_chunk, AIMessageChunk):
            if message_chunk.response_metadata:
                finish_reason = message_chunk.response_metadata.get("finish_reason", "")
                if finish_reason == "tool_calls":
                    yield "\n\n"

            if message_chunk.tool_call_chunks:
                tool_chunk = message_chunk.tool_call_chunks[0]
                tool_name = tool_chunk.get("name", "")
                if tool_name:
                    yield f"\n\n< TOOL CALL: {tool_name} >\n\n"
            else:
                yield message_chunk.content
            continue


mcp_client = None

async def get_mcp_client():
    global mcp_client
    if mcp_client is None:
        mcp_client = MultiServerMCPClient(
            # {
        # "filesystem": {
        #     "transport": "stdio",
        #     "command": "npx",
        #     "args": [
        #         "-y",
        #         "@modelcontextprotocol/server-filesystem",
        #         "D:/Shi-SF-Agent/saleforce-Agent/org_2/force-app/main/default/objects/Account/fields"
        #     ]
        # }
    # }
    {
    "weather": {
        "transport": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "C:/Users/lenovo/Desktop/Weather_MCP/weather",
        "run",
        "weather.py"
      ]
    }
}
        )
    return mcp_client

# async def client_input(user_input: str):
#     """
#     Initialize the MCP client and run the agent conversation loop.

#     The MultiServerMCPClient allows connection to multiple MCP servers using a single client and config.
#     """
#     try:
#         print("User_input", user_input)
#         client = await get_mcp_client()
#         print("User_input", user_input)
#         # Get tools and build graph
#         tools = await client.get_tools()
#         print("User_input", user_input)
#         graph = await build_agent_graph(tools=tools)
#         print("TOOLS", tools)
#         print("User_input", user_input)
#         # Pass a config with a thread_id to use memory
#         graph_config = {
#             "configurable": {
#                 "thread_id": "2"
#             }
#         }
#         print("User_input", user_input)
#         # Collect all response chunks
#         # try:
#         #     full_response = ""
#         #     async for response in stream_graph_response(
#         #         input=State(messages=[HumanMessage(content=user_input)]),
#         #         graph=graph, 
#         #         config=graph_config
#         # ):
#         #         full_response += str(response)
#         #         print("FULL RESPONSE\n", full_response)
#         #         return full_response
#         try:
#             input_message = [HumanMessage(content=user_input)]
#             output_message = graph.ainvoke({'messages': input_message}, config=graph_config)

#             for m in output_message['messages']:
#                 m.pretty_print()
#         except Exception as e:
#             print(f"Error in client_input: {str(e)}")
#     except Exception as e:
#         print("\n🔥 REAL ERROR TRACEBACK 🔥")
#         print(traceback.format_exc())
#         raise
        


async def client_input(user_input: str):
    try:
        client = await get_mcp_client()

        tools = await client.get_tools()
        graph = await build_agent_graph(tools=tools)

        graph_config = {
            "configurable": {
                "thread_id": "3"
            }
        }

        input_message = [HumanMessage(content=user_input)]

        output_message = await graph.ainvoke(
            {'messages': input_message},
            config=graph_config
        )

        for m in output_message['messages']:
            m.pretty_print()

    except Exception:
        print("\n🔥 REAL ERROR TRACEBACK 🔥")
        print(traceback.format_exc())
        raise



if __name__ == "__main__":

    import asyncio
    asyncio.run(client_input("who are you?"))
    # asyncio.run(client_input("Alter the backgorund color to purple"))
    # asyncio.run(client_input("what are the files present in the directory"))
    # asyncio.run(client_input("write a file named test.txt with greetings message"))
    # asyncio.run(client_input("create a new object named Mall with fields area and location"))

    # asyncio.run(client_input("What are the active weather alerts in Texas?"))