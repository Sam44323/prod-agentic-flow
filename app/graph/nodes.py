from app.graph.state import AgentState
from app.llm.qwen import get_llm, generate
from langchain_core.messages import HumanMessage, AIMessage
from app.tools.calculator import calculator
from app.tools.weather import get_weather


# LLM-Node for query and response with the language-model
def llm_node(state: AgentState) -> AgentState:
    llm = get_llm()
    print(state)

    messages = state.get("messages", [])

    messages.append(
        HumanMessage(content=state["user_input"]),
    )

    response = generate(messages)

    messages.append(AIMessage(content=response))
    state["messages"] = messages
    state["final_answer"] = str(response)
    print("exiting the llm_node")

    return state


# Calculator-node for evaluating the expression
def calculator_node(state: AgentState) -> AgentState:
    expression = state["user_input"]
    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    messages = state.get("messages", [])
    messages.append(
        HumanMessage(content=f"Evaluating the expression: {expression}"),
    )

    # try to evaluate the expression based on the input if routed by the router
    try:
        messages.append(
            AIMessage(content=f"Evaluating the expression: {expression}"),
        )
        state["messages"] = messages
        state["final_answer"] = calculator(expression)
        state["tool_output"] = state["final_answer"]
        state["error"] = ""
    except Exception as e:
        messages.append(
            AIMessage(content=f"Error evaluating the expression: {expression}"),
        )
        state["messages"] = messages
        state["error"] = e  # type: ignore
        state["tool_output"] = state["final_answer"]
        state["final_answer"] = "Invalid expression."

    return state


# Weather-node for fetching the weathers
def weather_node(state: AgentState) -> AgentState:
    state["tool_name"] = "weather"
    # just hardcoding for now
    state["tool_input"] = "Lond"

    messages = state.get("messages", [])
    messages.append(
        HumanMessage(content=f"Fetching the weather for {state['tool_input']}"),
    )

    try:
        result = get_weather(
            latitude=51.5074,
            longitude=-0.1278,
        )

        messages.append(
            AIMessage(content=f"Fetching the weather for {state['tool_input']}"),
        )
        state["tool_output"] = result
        state["final_answer"] = result
        state["messages"] = messages
        state["error"] = ""

    except Exception as e:
        state["tool_output"] = ""
        state["error"] = str(e)
        messages.append(
            AIMessage(content=f"Error fetching the weather for {state['tool_input']}"),
        )
        state["messages"] = messages
        state["final_answer"] = f"Weather Tool Error: {e}"

    return state
