from app.graph.state import AgentState
from langchain_core.messages import AIMessage


def output_error_node(state: AgentState) -> AgentState:
    state["messages"].append(
        AIMessage(content="Sorry, I couldn't generate a valid response.")
    )

    return state
