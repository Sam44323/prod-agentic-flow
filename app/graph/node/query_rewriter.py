# this overall is a very simple rewriter that just replaces the query with the rewritten query in proper-format

from langchain_core.messages import HumanMessage, SystemMessage

from app.graph.state import AgentState
from app.llm.qwen import generate


SYSTEM_PROMPT = """
You are a query rewriting assistant.

Rewrite the user's latest question so it is optimal for semantic vector search.

Rules:
- Preserve the original intent.
- Resolve references where possible.
- Expand ambiguous phrases into explicit ones.
- Do NOT answer the question.
- Return ONLY the rewritten query.
""".strip()


def query_rewriter(state: AgentState) -> AgentState:
    messages = state["messages"]

    # Find the latest user message
    latest_user_message = next(
        message for message in reversed(messages) if isinstance(message, HumanMessage)
    )

    rewritten_query = generate(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=latest_user_message.content),
        ]
    )

    state["rewritten_query"] = rewritten_query.strip()

    return state
