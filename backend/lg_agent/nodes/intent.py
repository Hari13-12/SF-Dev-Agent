from lg_agent.core.state_model import State
from lg_agent.core.llm_manager import LLMManager
import json


def intent_classifier(state: State):
    print("Intent Classifier Node")
    prompt = """You are an Intent Analysis Agent.

Your job is to analyze the user query and determine the correct intent.
If the query represents a valid business request, return structured JSON data.
If the query is a greeting, small talk, or unrelated, return a general response.

Possible Intents

1) new_object -> User wants to create a new Salesforce object
Examples:
“Create a new custom object”
“I want a new object for invoices”
“Add a new object with fields”

Output Format:
{
    "intent":"new_object",
    "object_name":"<name_of_object>",
    "fields":["<field1>", "<field2>", "..."]
}

2) edit_object -> User wants to modify an existing Salesforce object
Includes:
Adding or updating fields
Modifying relationships
Updating existing object metadata
Examples:
“Add a field to Account”
“Update Opportunity object”
“Modify existing custom object”
“Which objects have a Master-Detail relationship to Meter__c?”

Output Format:
{
    "intent":"edit_object",
    "object_name":"<name_of_object>",
    "fields":["<fileds1>", "<modification2>", "..."]
}

3) general -> Greetings, small talk, or unrelated queries
Greetings, small talk, or unrelated queries
Questions not requesting object creation or modification
Examples:
“Hi”
“Hello”
“What is Salesforce?”
“What’s the weather?”

Output Format:
{
    "intent":"general"
}
"""
    # system_prompt = SystemMessage(content=prompt)
    # input_message = HumanMessage(content=user_query)
    llm = LLMManager().get_llm()
    # response = llm.invoke([system_prompt, input_message])
    response = llm.invoke(prompt + state["messages"][-1].content)
    response_content = response.content.replace("```json", "").replace("```", "")
    response_content = json.loads(response_content)
    print("Intent Classifier Response: ", response_content)
    state["intent"] = response_content["intent"]
    # state["obj_name"] = response_content["object_name"]
    return state
