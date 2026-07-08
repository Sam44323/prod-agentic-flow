from app.graph.state import AgentState


# routing the flow based on the user-input
def router(state: AgentState):
    print("Routing...")
    query = state["user_input"]

    if "+" in query:
        print("routing to calculator")
        return "calculator"

    print("routing to llm")
    return "llm"
