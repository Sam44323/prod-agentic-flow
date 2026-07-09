from app.graph.state import AgentState


def retriever_node(state: AgentState) -> AgentState:
    """
    Temporary retrieval node.

    TBD: an actual semantic search
    against a vector database.
    """

    state["retrieved_documents"] = [f"Retrieved context for: {state['user_input']}"]

    state["retrieval_attempts"] = state.get("retrieval_attempts", 0) + 1

    return state
