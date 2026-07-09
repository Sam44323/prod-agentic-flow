from app.graph.state import AgentState
from app.llm.qwen import llm

PLANNER_PROMPT = """
You are an Agentic RAG planner.

Decide whether answering the user's request requires retrieving external-knowledge.

Rules:

- If any external knowledge is needed, return:
retrieve

- Otherwise return:
answer

Return ONLY one word.

User:
{message}
"""


def planner_node(state: AgentState) -> AgentState:
    prompt = PLANNER_PROMPT.format(message=state["user_input"])
    response = llm.invoke(prompt)

    decision = str(response.content).strip().lower()

    state["planner_action"] = decision

    return state
