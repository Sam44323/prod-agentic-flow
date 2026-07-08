from app.graph.state import AgentState
from app.llm.qwen import get_llm
from app.tools.calculator import calculator
from app.tools.weather import get_weather


# LLM-Node for query and response with the language-model
def llm_node(state: AgentState) -> AgentState:
    llm = get_llm()
    print(state)

    response = llm.invoke(state["user_input"])

    state["final_answer"] = str(response.content)
    print("exiting the llm_node")

    return state


# Calculator-node for evaluating the expression
def calculator_node(state: AgentState) -> AgentState:
    expression = state["user_input"]
    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    # try to evaluate the expression based on the input if routed by the router
    try:
        state["final_answer"] = calculator(expression)
        state["tool_output"] = state["final_answer"]
        state["error"] = ""
    except Exception as e:
        state["error"] = e  # type: ignore
        state["tool_output"] = state["final_answer"]
        state["final_answer"] = "Invalid expression."

    return state


# Weather-node for fetching the weathers
def weather_node(state: AgentState) -> AgentState:
    state["tool_name"] = "weather"
    # just hardcoding for now
    state["tool_input"] = "Lond"

    try:
        result = get_weather(
            latitude=51.5074,
            longitude=-0.1278,
        )

        state["tool_output"] = result
        state["final_answer"] = result
        state["error"] = ""

    except Exception as e:
        state["tool_output"] = ""
        state["error"] = str(e)
        state["final_answer"] = f"Weather Tool Error: {e}"

    return state
