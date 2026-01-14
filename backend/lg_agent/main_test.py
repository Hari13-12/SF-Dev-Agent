# from lg_agent.workflow.graph_builer import builder
# from anyio.lowlevel import checkpoint
from langchain_core.messages import HumanMessage
from lg_agent.workflow.graph_builder_client_2 import build_graph
import asyncio
    






async def main(user_query: str):

    graph = await build_graph()
    # builder = graph.compile(checkmemory)
    graph_config = {
            "configurable": {
                "thread_id": "1"
            }
        }
    input_message = [HumanMessage(content=user_query)]
    output_message = await graph.ainvoke({'messages': input_message}, config = graph_config)  # Remove await here

    for m in output_message['messages']:
        m.pretty_print()
    
if __name__ == "__main__":
    # asyncio.run(main("Hello"))
    asyncio.run(main("what are the accounts connected to my org"))
