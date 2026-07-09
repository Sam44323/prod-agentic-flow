from app.graph.state import AgentState


def calculator_request_node(state: AgentState) -> AgentState:
    expression = state["user_input"]

    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    state["approval_required"] = True
    state["approval_reason"] = f"Execute calculator: {expression}"

    return state
