from app.graph.state import AgentState
from app.guardrails.policy_engine import PolicyEngine

policy_engine = PolicyEngine()


def guardrail_node(state: AgentState) -> AgentState:
    message = state["user_input"]

    blocked, reason = policy_engine.validate_input(str(message))

    state["guardrail_passed"] = not blocked
    state["guardrail_reason"] = reason

    return state
