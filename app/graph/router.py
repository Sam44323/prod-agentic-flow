from app.graph.state import AgentState


# routing the flow based on the user-input
def router(state: AgentState):
    query = state["user_input"]

    if "+" in query:
        return "calculator"

    return "llm"
