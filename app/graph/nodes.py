from app.graph.state import AgentState
from langgraph.types import interrupt
from app.llm.qwen import generate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.tools.calculator import calculator
from app.tools.weather import get_weather
from app.memory.fact_extractor import extract_facts
from app.memory.semantic_memory import SemanticMemory
from langgraph.graph import END


semantic_memory = SemanticMemory()


SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "reveal your prompt",
    "developer message",
    "repeat your instructions",
]


def is_suspicious_prompt(message: str) -> tuple[bool, str]:
    text = message.lower()

    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in text:
            return True, f"Matched pattern: {pattern}"

    return False, ""


def validate_output(text: str) -> tuple[bool, str]:
    if not text.strip():
        return False, "Empty response"

    if len(text) > 8000:
        return False, "Response too large"

    return True, ""


# LLM-Node for query and response with the language-model
def llm_node(state: AgentState) -> AgentState:
    print(state)

    messages = state.get("messages", [])

    messages.append(
        HumanMessage(content=state["user_input"]),
    )

    # extracting the facts from the user-input
    facts = extract_facts(state["user_input"])

    session_id = "default"  # Will become dynamic overall later

    for key, value in facts.items():
        semantic_memory.save_fact(
            session_id=session_id,
            key=key,
            value=value,
        )

    # retrieving the facts from the semantic-memory
    session_id = "default"

    facts = semantic_memory.get_all_facts(session_id)

    # adding the facts to the context
    if facts:
        memory_context = "\n".join(f"{key}: {value}" for key, value in facts.items())

        messages.insert(
            0,
            SystemMessage(content=f"Known facts about the user:\n{memory_context}"),
        )

    response = generate(messages)

    messages.append(AIMessage(content=response))
    state["messages"] = messages
    state["final_answer"] = response
    print("exiting the llm_node")

    return state


# Calculator-node for evaluating the expression
def calculator_node(state: AgentState) -> AgentState:
    expression = state["user_input"]
    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    messages = state.get("messages", [])
    messages.append(
        HumanMessage(content=f"{expression}"),
    )

    # try to evaluate the expression based on the input if routed by the router
    try:
        response = calculator(expression)
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
        HumanMessage(content=f"{state['tool_input']}"),
    )

    try:
        result = get_weather(
            latitude=51.5074,
            longitude=-0.1278,
        )

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


# Interruption-node for handling the interruption options
def approval_node(state: AgentState) -> AgentState:
    # when interrupt is invoked, langgraph saves the checkpoint
    # execution pauses overall and waits for the interruption
    # and once done with the interruption, it resumes the execution
    approved = interrupt(
        {
            "message": "Approve this action?",
            "reason": state.get("approval_reason", ""),
        }
    )

    state["approval_granted"] = approved
    return state


# Calculator-node for evaluating the expression
def calculator_request_node(state: AgentState) -> AgentState:
    expression = state["user_input"]

    state["tool_name"] = "calculator"
    state["tool_input"] = expression

    # For demo purposes, always require approval.
    # Later this can depend on risk, user role, etc.
    state["approval_required"] = True
    state["approval_reason"] = f"Execute calculator: {expression}"

    return state


# Interruption-node for handling the interruption options
def post_approval_route(state: AgentState) -> str:
    if state["approval_granted"]:
        return "calculator"
    return END


# Guardrail-node for handling the guardrails
def guardrail_node(state: AgentState) -> AgentState:
    message = state["messages"][-1].content

    blocked, reason = is_suspicious_prompt(str(message))

    state["guardrail_passed"] = not blocked
    state["guardrail_reason"] = reason

    return state


def guardrail_response_node(state: AgentState) -> AgentState:
    state["messages"].append(
        AIMessage(
            content=(
                "I can't help with requests that attempt to reveal "
                "internal instructions, bypass safety mechanisms, or "
                "otherwise violate my operating policies."
            )
        )
    )

    return state


def output_guardrail_node(state: AgentState) -> AgentState:
    response = state["messages"][-1].content

    valid, reason = validate_output(str(response))

    state["output_valid"] = valid
    state["output_validation_reason"] = reason

    return state


def output_error_node(state: AgentState) -> AgentState:
    state["messages"].append(
        AIMessage(content="Sorry, I couldn't generate a valid response.")
    )

    return state
