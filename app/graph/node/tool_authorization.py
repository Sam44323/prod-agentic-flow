from app.graph.state import AgentState
from app.graph.dependencies import policy_engine


def tool_authorization_node(state: AgentState) -> AgentState:
    tool = state.get("tool_name")

    authorized, reason = policy_engine.authorize_tool(tool)

    state["tool_authorization"] = authorized
    state["tool_authorization_reason"] = reason

    return state
