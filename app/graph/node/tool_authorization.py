from app.graph.state import AgentState
from app.guardrails.policy_engine import PolicyEngine

policy_engine = PolicyEngine()


def tool_authorization_node(state: AgentState) -> AgentState:
    tool = state.get("tool_name")

    authorized, reason = policy_engine.authorize_tool(tool)

    state["tool_authorization"] = authorized
    state["tool_authorization_reason"] = reason

    return state
