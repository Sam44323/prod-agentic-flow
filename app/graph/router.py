import re

from app.graph.state import AgentState


def route(state: AgentState) -> str:
    """
    Decide which node should execute next.
    """

    user_input = state["user_input"].strip().lower()

    # Simple math-detection
    if re.fullmatch(r"[0-9+\-*/().\s]+", user_input):
        return "calculator_request"

    # Weather-text detection
    if "weather" in user_input:
        return "weather"

    return "llm"


def approval_route(state: AgentState) -> str:
    if state.get("approval_required", False):
        return "approval"
    return "calculator"
