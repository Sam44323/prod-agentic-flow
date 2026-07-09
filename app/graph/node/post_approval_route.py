from app.graph.state import AgentState
from langgraph.graph import END


def post_approval_route(state: AgentState) -> str:
    if state["approval_granted"]:
        return "calculator"
    return END
