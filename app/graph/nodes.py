from app.graph.state import AgentState
from app.llm.qwen import get_llm

 # LLM-Node for query and response with the language-model
def llm_node(state: AgentState) -> AgentState:
    llm = get_llm()

    response = llm.invoke(state["user_input"])

    state["final_answer"] = response.content

    return state

