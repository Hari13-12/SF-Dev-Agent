from lg_agent.workflow.graph_builer import builder
from langchain_core.messages import HumanMessage

    
def main(user_query: str):
    graph = builder.compile()
    input_message = [HumanMessage(content=user_query)]
    output_message = graph.invoke({'messages': input_message})

    for m in output_message['messages']:
        m.pretty_print()
    
if __name__ == "__main__":
    # main("Create a new custom object called City with fields Location and Area")
    # main("Hello")
    main("alter a new field in meter reading object with fied name as house number")
