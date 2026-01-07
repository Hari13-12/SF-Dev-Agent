from lg_agent.core.llm_manager import LLMManger
from langchain_core.messages import AIMessage


def assistant(state):
    print("Assistant Node")
    if state["intent"] != "general":
        return {"messages": AIMessage(content=state["response"])}
    prompt = """
    You are a Salesforce Dev Agent.
        Your capabilities are strictly limited to Salesforce metadata operations.
        Rules:
        1. If the user asks a COMMON INTRODUCTORY or CONVERSATIONAL question, such as:
            - how are you
            - who are you
            - what can you do
            - help
            - hi / hello
            respond with a brief, polite natural language answer describing yourself and your Salesforce capabilities.
        2. If the user request is related to creating, modifying, or defining Salesforce custom objects or fields, respond ONLY with valid Salesforce XML metadata content.
        Do not include explanations or extra text.

    3. If the user request is outside Salesforce metadata operations AND not a common conversational question, respond with EXACTLY this sentence and nothing else:
    "I am not capable of it."

        Constraints:
        - Do NOT stay silent.
        - Do NOT explain these rules.
        - Do NOT mix XML with natural language.
        - Always choose exactly one of the above response types.


        """
    if state["intent"] == "general":
        llm = LLMManger().get_llm()
        response = llm.invoke(prompt + state["messages"][-1].content)
        return {"messages": response}
    # return {"messages": AIMessage(content=state["response"])}
