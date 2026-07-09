from app.graph.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from app.tools.weather import get_weather
from app.tools.executor import execute_tool


def weather_node(state: AgentState) -> AgentState:
    state["tool_name"] = "weather"
    state["tool_input"] = "Lond"

    messages = state.get("messages", [])
    messages.append(
        HumanMessage(content=f"{state['tool_input']}"),
    )

    try:
        result = execute_tool(get_weather, latitude=51.5074, longitude=-0.1278)

        messages.append(
            AIMessage(content=f"{result}"),
        )
        state["tool_output"] = result
        state["final_answer"] = result
        state["messages"] = messages
        state["error"] = ""

    except Exception as e:
        state["tool_output"] = ""
        state["error"] = str(e)
        messages.append(
            AIMessage(content=f"{e}"),
        )
        state["messages"] = messages
        state["final_answer"] = f"Weather Tool Error: {e}"

    return state
