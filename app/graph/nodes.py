from app.graph.state import AgentState
from app.llm.qwen import get_llm
from app.tools.calculator import calculator


# LLM-Node for query and response with the language-model
def llm_node(state: AgentState) -> AgentState:
    llm = get_llm()
    print(state)

    response = llm.invoke(state["user_input"])

    state["final_answer"] = str(response.content)
    print("exiting the llm_node")

    return state


# Calculator-Node for evaluating the expression
def calculator_node(state: AgentState) -> AgentState:
    expression = state["user_input"]

    # try to evaluate the expression based on the input if routed by the router
    try:
        state["final_answer"] = calculator(expression)
    except Exception:
        state["final_answer"] = "Invalid expression."

    return state
