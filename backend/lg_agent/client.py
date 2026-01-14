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
    # "weather": {
    #     "transport": "stdio",
    #   "command": "uv",
    #   "args": [
    #     "--directory",
    #     "C:/Users/lenovo/Desktop/Weather_MCP/weather",
    #     "run",
    #     "weather.py"
    #   ]
    # }

		"salesforce": {
			"command": "npx",
            "transport": "stdio",
			"args": [
				"-y",
				"@salesforce/mcp",
				"--orgs",
				"DEFAULT_TARGET_ORG",
				"--toolsets",
				"all"
			]
		}
	}
        )
    return mcp_client


async def client_input(user_input: str):
    try:
        client = await get_mcp_client()

        tools = await client.get_tools()
        print(type(tools))
        print("MCP TOOLS", tools)
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
    # asyncio.run(client_input("who are you?"))
    # asyncio.run(client_input("Alter the backgorund color to purple"))
    # asyncio.run(client_input("what are the files present in the directory"))
    # asyncio.run(client_input("write a file named test.txt with greetings message"))
    # asyncio.run(client_input("create a new object named Mall with fields area and location"))

    # asyncio.run(client_input("What are the active weather alerts in Texas?"))
    # asyncio.run(client_input("how many objects i have in my org"))
    # asyncio.run(client_input("give the object names present in my org"))
    asyncio.run(client_input("what are the accounts connected to my org"))