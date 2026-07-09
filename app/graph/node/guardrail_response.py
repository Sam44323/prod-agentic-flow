from app.graph.state import AgentState
from langchain_core.messages import AIMessage


def guardrail_response_node(state: AgentState) -> AgentState:
    state["messages"].append(
        AIMessage(
            content=(
                "I can't help with requests that attempt to reveal "
                "internal instructions, bypass safety mechanisms, or "
                "otherwise violate my operating policies."
            )
        )
    )

    return state
