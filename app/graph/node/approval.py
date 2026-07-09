from app.graph.state import AgentState
from langgraph.types import interrupt


def approval_node(state: AgentState) -> AgentState:
    approved = interrupt(
        {
            "message": "Approve this action?",
            "reason": state.get("approval_reason", ""),
        }
    )

    state["approval_granted"] = approved
    return state
