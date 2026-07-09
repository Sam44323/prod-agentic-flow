from app.graph.state import AgentState
from langchain_core.messages import HumanMessage, AIMessage
from app.tools.calculator import calculator
from app.tools.executor import execute_tool


def calculator_node(state: AgentState) -> AgentState:
    expression = state["user_input"]
    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    messages = state.get("messages", [])
    messages.append(
        HumanMessage(content=f"{expression}"),
    )

    try:
        response = execute_tool(calculator, expression)
        messages.append(
            AIMessage(content=f"{response}"),
        )
        state["messages"] = messages
        state["final_answer"] = response
        state["tool_output"] = state["final_answer"]
        state["error"] = ""
    except Exception as e:
        messages.append(
            AIMessage(content=f"{expression}"),
        )
        state["messages"] = messages
        state["error"] = e
        state["tool_output"] = state["final_answer"]
        state["final_answer"] = "Invalid expression."

    return state
