import re

from app.graph.state import AgentState
from typing import Literal

MAX_RETRIEVAL_ATTEMPTS = 3


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


# planner-router
def planner_router(state: AgentState) -> str:
    """
    Routes execution based on the planner's decision.
    """

    action = state.get("planner_action", "llm")

    if action == "weather":
        return "weather"

    if action == "calculator":
        return "calculator_request"

    if action == "retrieve":
        return "retrieve"

    return "llm"


def approval_route(state: AgentState) -> str:
    if state.get("approval_required", False):
        return "approval"
    return "calculator"


def guardrail_router(
    state: AgentState,
) -> Literal["route", "guardrail_response"]:
    if state["guardrail_passed"]:
        return "route"

    return "guardrail_response"


def output_router(
    state: AgentState,
) -> Literal["__end__", "output_error"]:
    if state["output_valid"]:
        return "__end__"

    return "output_error"


def tool_authorization_router(
    state: AgentState,
) -> Literal["execute_tool", "tool_denied"]:
    if state["tool_authorized"]:
        return "execute_tool"

    return "tool_denied"


def retrieval_router(
    state: AgentState,
) -> Literal["llm", "query_rewriter"]:
    if state.get("retrieval_sufficient", False):
        return "llm"

    if state.get("retrieval_attempts", 0) >= MAX_RETRIEVAL_ATTEMPTS:
        return "llm"

    return "query_rewriter"
