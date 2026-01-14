# # import asyncio
# # from langchain_mcp_adapters.client import MultiServerMCPClient



# # async def get_mcp_tools():
# #         mcp_client = MultiServerMCPClient(
# #             # {
# #         # "filesystem": {
# #         #     "transport": "stdio",
# #         #     "command": "npx",
# #         #     "args": [
# #         #         "-y",
# #         #         "@modelcontextprotocol/server-filesystem",
# #         #         "D:/Shi-SF-Agent/saleforce-Agent/org_2/force-app/main/default/objects/Account/fields"
# #         #     ]
# #         # }
# #     # }
# #     {
# #     # "weather": {
# #     #     "transport": "stdio",
# #     #   "command": "uv",
# #     #   "args": [
# #     #     "--directory",
# #     #     "C:/Users/lenovo/Desktop/Weather_MCP/weather",
# #     #     "run",
# #     #     "weather.py"
# #     #   ]
# #     # }

# # 		"salesforce": {
# # 			"command": "npx",
# #             "transport": "stdio",
# # 			"args": [
# # 				"-y",
# # 				"@salesforce/mcp",
# # 				"--orgs",
# # 				"DEFAULT_TARGET_ORG",
# # 				"--toolsets",
# # 				"all"
# # 			]
# # 		}
# # 	}
# #         )
# #         return mcp_client.get_tools()



# # async def _load_tools():
# #     try:
# #         client = await get_mcp_client()
# #         tools = await client.get_tools()
# #         print("Successfully fetche MCP tools")
# #         return tools
# #     except Exception as e:
# #         print(f"Failed to fetch MCP tools: {e}")
# #         return None

# # def get_mcp_tools():
# #     """
# #     Synchronously accessible MCP tools.
# #     Loads tools once and keeps them alive in memory.
# #     """
# #     global _mcp_tools
# #     try:
# #         if _mcp_tools is None:
# #             _mcp_tools = asyncio.run(_load_tools())
# #         print("Successfully loaded MCP tools")
# #         return _mcp_tools
# #     except Exception as e:
# #         print(f"Failed to load MCP tools: {e}")
# #         return None



# # from langchain_mcp_adapters.client import MultiServerMCPClient

# # _mcp_tools = None
# # _mcp_client = None


# # async def init_mcp_tools():
# #     """
# #     Initialize MCP client and tools ONCE.
# #     Must be called inside an active event loop (FastAPI startup).
# #     """
# #     global _mcp_client, _mcp_tools

# #     if _mcp_tools is not None:
# #         return _mcp_tools

# #     _mcp_client = MultiServerMCPClient(
# #         {
# #             "salesforce": {
# #                 "command": "npx",
# #                 "transport": "stdio",
# #                 "args": [
# #                     "-y",
# #                     "@salesforce/mcp",
# #                     "--orgs",
# #                     "DEFAULT_TARGET_ORG",
# #                     "--toolsets",
# #                     "all"
# #                 ]
# #             }
# #         }
# #     )

# #     _mcp_tools = await _mcp_client.get_tools()
# #     print("✅ MCP tools initialized")

# #     return _mcp_tools


# # def get_mcp_tools():
# #     """
# #     SAFE synchronous accessor.
# #     Tools MUST be initialized first via init_mcp_tools().
# #     """
# #     if _mcp_tools is None:
# #         raise RuntimeError(
# #             "MCP tools not initialized. "
# #             "Call init_mcp_tools() during FastAPI startup."
# #         )
# #     return _mcp_tools



# import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def get_mcp_tools():
    mcp_client = MultiServerMCPClient(
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
    # Await get_tools() since it's async
    tools = await mcp_client.get_tools()
    print(tools)
    print("Success")
    return tools

# if __name__ == "__main__":
#     asyncio.run(get_mcp_tools())




import pandas as pd
import json

def extract_args_schema(tool):
    args = getattr(tool, "args_schema", None)

    # Case 1: Pydantic model
    if hasattr(args, "schema"):
        return args.schema()

    # Case 2: Already a dict (MCP tools)
    if isinstance(args, dict):
        return args

    # Case 3: None / unknown
    return {}


def mcp_tools_to_excel(tools, output_file="mcp_tools.xlsx"):
    rows = []

    for tool in tools:
        rows.append({
            "tool_name": getattr(tool, "name", ""),
            "description": getattr(tool, "description", ""),
            "resources": json.dumps(
                extract_args_schema(tool),
                indent=2
            )
        })

    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)

    print(f"✅ Excel generated: {output_file}")
    print(f"🛠️ Total MCP tools exported: {len(rows)}")



async def main():
    mcp_tools = await get_mcp_tools()
    mcp_tools_to_excel(mcp_tools, "salesforce_mcp_tools.xlsx")

import asyncio
if __name__ == "__main__":
    asyncio.run(main())