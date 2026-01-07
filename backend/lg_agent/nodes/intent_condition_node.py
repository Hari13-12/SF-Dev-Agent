from lg_agent.core.state_model import State

def intent_condition(state: State):
    print("Intent Condition Node:", state["intent"])
    if state["intent"] == "new_object":
        return {"next_node": "new_object_node"}
    if state["intent"] == "edit_object":
        return {"next_node": "edit_object_node"}    
    if state["intent"] == "general":
        return {"next_node": "assistant"}