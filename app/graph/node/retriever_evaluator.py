from langchain_core.messages import HumanMessage, SystemMessage

from app.graph.state import AgentState
from app.llm.qwen import generate


SYSTEM_PROMPT = """
You evaluate retrieval quality.

Given:
- the user's question
- the retrieved documents

Return ONLY:

yes

or

no

Return "yes" only if the documents contain enough information to answer the question.
""".strip()


def retrieval_evaluator_node(state: AgentState) -> AgentState:
    query = state.get("rewritten_query") or state["user_input"]

    documents = "\n\n".join(state.get("retrieved_documents", []))

    response = generate(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=f"""
                    Question:
                    {query}

                    Retrieved Documents:
                    {documents}
                    """.strip()
            ),
        ]
    )

    state["retrieval_sufficient"] = response.strip().lower() == "yes"

    return state
