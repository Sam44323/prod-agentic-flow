from app.graph.state import AgentState
from app.retrieval.retriever import retrieve


# retriver-node for retrieving the relevant documents for the system
def retriever_node(state: AgentState) -> AgentState:
    query = state.get("rewritten_query") or state["user_input"]

    documents = retrieve(query)

    state["retrieved_documents"] = [document.page_content for document in documents]

    state["retrieval_attempts"] = state.get("retrieval_attempts", 0) + 1

    state["retrieval_success"] = len(documents) > 0

    return state

