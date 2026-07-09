from app.graph.state import AgentState
from app.graph.dependencies import policy_engine


def guardrail_node(state: AgentState) -> AgentState:
    message = state["user_input"]

    blocked, reason = policy_engine.validate_input(str(message))

    state["guardrail_passed"] = not blocked
    state["guardrail_reason"] = reason

    return state
