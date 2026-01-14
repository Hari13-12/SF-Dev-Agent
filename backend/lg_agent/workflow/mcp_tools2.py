from langchain_core.tools import StructuredTool
from pydantic import create_model
from typing import List
import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient

# ---------- Global cache ----------
_mcp_client: MultiServerMCPClient | None = None
_structured_tools: List[StructuredTool] | None = None
_lock = asyncio.Lock()


# ---------- Single public function ----------
async def get_structured_mcp_tools() -> List[StructuredTool]:
    """
    One-call API:
    - Initializes MCP (once)
    - Fetches MCP tools
    - Converts them to LangChain StructuredTools
    - Returns cached tools
    """
    global _mcp_client, _structured_tools

    if _structured_tools is not None:
        return _structured_tools

    async with _lock:
        if _structured_tools is not None:
            return _structured_tools

        print("Initializing MCP tools (one-time)")

        _mcp_client = MultiServerMCPClient(
            {
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

        mcp_tools = await _mcp_client.get_tools()
        _structured_tools = [
            _convert_mcp_to_structured_tool(tool, _mcp_client)
            for tool in mcp_tools
        ]

        print(f"Loaded {len(_structured_tools)} MCP tools")
        return _structured_tools


# ---------- Internal converter ----------
def _convert_mcp_to_structured_tool(mcp_tool, mcp_client: MultiServerMCPClient) -> StructuredTool:
    tool_name = mcp_tool.name
    tool_description = mcp_tool.description or f"MCP tool: {tool_name}"

    # It's args_schema, not input_schema!
    input_schema_dict = mcp_tool.args_schema or {}
    
    properties = input_schema_dict.get("properties", {})
    required = input_schema_dict.get("required", [])

    fields = {}
    for name, info in properties.items():
        field_type = str
        match info.get("type"):
            case "boolean":
                field_type = bool
            case "integer":
                field_type = int
            case "number":
                field_type = float

        default = ... if name in required else None
        fields[name] = (field_type, default)

    ArgsSchema = create_model(f"{tool_name}_Args", **fields)

    async def tool_coroutine(**kwargs) -> str:
        try:
            result = await mcp_client.call_tool(
                tool_name,
                arguments=kwargs
            )

            if hasattr(result, "content") and result.content:
                content = result.content[0]
                if hasattr(content, "text"):
                    return str(content.text)

            return str(result)

        except Exception as e:
            return f"Error calling {tool_name}: {e}"

    return StructuredTool(
        name=tool_name,
        description=tool_description,
        args_schema=ArgsSchema,
        coroutine=tool_coroutine,
        return_direct=False
    )