from app.graph.state import AgentState


def retriever_node(state: AgentState) -> AgentState:
    """
    Temporary retrieval node.

    TBD: Replace with semantic search against a vector database.
    """

    # geting rewritten query if it exists, otherwise use the user-input as fallback data
    query = state.get("rewritten_query") or state["user_input"]

    state["retrieved_documents"] = [f"Retrieved context for: {query}"]

    state["retrieval_attempts"] = state.get("retrieval_attempts", 0) + 1

    return state
